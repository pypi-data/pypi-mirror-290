import torch
import torch.nn as nn
import torch.nn.functional as F
import random as random


class MGDCR(nn.Module):
    def __init__(self, cfg):
        super(MGDCR, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        # self.criteria = nn.BCEWithLogitsLoss()
        # self.xent = nn.CrossEntropyLoss()
        # self.sigm = nn.Sigmoid()

        self.MLP1 = make_mlplayers(cfg.dataset.ft_size, cfg.mgdcr.mlp_cfg)
        self.MLP2 = make_mlplayers(cfg.dataset.ft_size, cfg.mgdcr.mlp_cfg)
        self.MLP3 = make_mlplayers(cfg.dataset.ft_size, cfg.mgdcr.mlp_cfg)
        # length = args.length
        self.w_list = nn.ModuleList([nn.Linear(cfg.mgdcr.mlp_cfg[-1], cfg.mgdcr.mlp_cfg[-1], bias=True) for _ in range(cfg.dataset.num_view)])
        self.y_list = nn.ModuleList([nn.Linear(cfg.mgdcr.mlp_cfg[-1], 1) for _ in range(cfg.dataset.num_view)])
        self.W = nn.Parameter(torch.zeros(size=(cfg.dataset.num_view * cfg.mgdcr.mlp_cfg[-1], cfg.mgdcr.mlp_cfg[-1])))
        self.att_act1 = nn.Tanh()
        self.att_act2 = nn.Softmax(dim=-1)
        # if args.isSemi:
        #     self.logistic = LogReg(cfg[-1], args.nb_classes).to(args.device)
        self.encoder = nn.ModuleList()
        self.encoder.append(self.MLP1)
        self.encoder.append(self.MLP2)
        self.encoder.append(self.MLP3)


    def forward(self, data):
        x = F.dropout(data.features, self.args.gnn.dropout, training=self.training)
        h_p_list = []
        h_a_list = []
        for i in range(self.args.dataset.num_view):
            h_a = self.encoder[i](x)
            if self.args.dataset.sparse:
                h_p = torch.spmm(data.adj_list[i], h_a)
            else:
                h_p = torch.mm(data.adj_list[i], h_a)
            h_a_list.append(h_a)
            h_p_list.append(h_p)

        # if self.args.isSemi:
        #     h_fusion = self._combine_att(h_p_list)
        #     semi = self.logistic(h_fusion).squeeze(0)
        # else:
        #     semi = 0
        loss_inter = 0
        loss_intra = 0
        for i in range(self.args.dataset.num_view):
            intra_c = (h_p_list[i]).T @ (h_a_list[i])
            on_diag_intra = torch.diagonal(intra_c).add_(-1).pow_(2).sum()
            off_diag_intra = off_diagonal(intra_c).pow_(2).sum()
            loss_intra += (on_diag_intra + self.args.mgdcr.lambdintra[i] * off_diag_intra) * self.args.mgdcr.w_intra[i]
            if i == 1 and self.args.dataset.num_view == 2:
                break
            inter_c = (h_p_list[i]).T @ (h_p_list[(i + 1) % self.args.dataset.num_view])
            on_diag_inter = torch.diagonal(inter_c).add_(-1).pow_(2).sum()
            off_diag_inter = off_diagonal(inter_c).pow_(2).sum()
            loss_inter += (on_diag_inter + self.args.mgdcr.lambdinter[i] * off_diag_inter) * self.args.mgdcr.w_inter[i]

        loss = loss_intra + loss_inter
        return loss

    def get_embedding(self, data):
        h_p_list = []
        for i in range(self.args.dataset.num_view):
            h_a = self.encoder[i](data.features)
            if self.args.dataset.sparse:
                h_p = torch.spmm(data.adj_list[i], h_a)
            else:
                h_p = torch.mm(data.adj_list[i], h_a)
            h_p_list.append(h_p)
        h_fusion = self._combine_att(h_p_list)

        return  h_fusion.detach()

    def preprocess(self, data):
        data.features = data.features.to(self.device)
        data.adj_list = [adj.to(self.device) for adj in data.adj_list]

    def postprocess(self, data):
        pass

    def _combine_att(self, h_list):
        h_combine_list = []
        for i, h in enumerate(h_list):
            h = self.w_list[i](h)
            h = self.y_list[i](h)
            h_combine_list.append(h)
        score = torch.cat(h_combine_list, -1)
        score = self.att_act1(score)
        score = self.att_act2(score)
        score = torch.unsqueeze(score, -1)
        h = torch.stack(h_list, dim=1)
        h = score * h
        h = torch.sum(h, dim=1)
        return h
    

def make_mlplayers(in_channel, cfg, batch_norm=False, out_layer =None):
    layers = []
    in_channels = in_channel
    layer_num  = len(cfg)
    for i, v in enumerate(cfg):
        out_channels =  v
        mlp = nn.Linear(in_channels, out_channels)
        if batch_norm:
            layers += [mlp, nn.BatchNorm1d(out_channels, affine=False), nn.ReLU()]
        elif i != (layer_num-1):
            layers += [mlp, nn.ReLU()]
        else:
            layers += [mlp]
        in_channels = out_channels
    if out_layer != None:
        mlp = nn.Linear(in_channels, out_layer)
        layers += [mlp]
    return nn.Sequential(*layers)#, result

def off_diagonal(x):
    # return a flattened view of the off-diagonal elements of a square matrix
    n, m = x.shape
    assert n == m
    return x.flatten()[:-1].view(n - 1, n + 1)[:, 1:].flatten()