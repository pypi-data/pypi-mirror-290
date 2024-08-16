import torch
import torch.nn as nn
import numpy as np
import random as random

from models.HDMI_utils import GCN, InterDiscriminator


class HDMI(nn.Module):
    def __init__(self, cfg):
        super(HDMI, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.gcn_list = nn.ModuleList([GCN(cfg.dataset.ft_size, cfg.gnn.hidden_dim) for _ in range(cfg.dataset.num_view)])
        self.w_list = nn.ModuleList([nn.Linear(cfg.gnn.hidden_dim, cfg.gnn.hidden_dim, bias=False) for _ in range(cfg.dataset.num_view)])
        self.y_list = nn.ModuleList([nn.Linear(cfg.gnn.hidden_dim, 1) for _ in range(cfg.dataset.num_view)])
        self.disc_layers = InterDiscriminator(cfg.gnn.hidden_dim, cfg.dataset.ft_size)
        if cfg.hdmi.same_discriminator:
            self.disc_fusion = self.disc_layers
        else:
            self.disc_fusion = InterDiscriminator(cfg.gnn.hidden_dim, cfg.dataset.ft_size)
        self.att_act1 = nn.Tanh()
        self.att_act2 = nn.Softmax(dim=-1)
        self.criteria = nn.BCEWithLogitsLoss()

        self.init_weight()
    
    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0) 

    def forward(self, data):
        # corruption function
        idx = np.random.permutation(self.args.dataset.nb_nodes)
        shuf_fts = data.features[idx, :].to(self.device)

        h_1_list = []
        h_2_list = []
        c_list = []

        logits_e_list = []
        logits_i_list = []
        logits_j_list = []
        for i, adj in enumerate(data.adj_list):
            # real samples
            h_1 = torch.squeeze(self.gcn_list[i](data.features, adj, self.args.dataset.sparse))
            h_1_list.append(h_1)
            c = torch.squeeze(torch.mean(h_1, 0))   # readout
            c_list.append(c)

            # negative samples
            h_2 = torch.squeeze(self.gcn_list[i](shuf_fts, adj, self.args.dataset.sparse))
            h_2_list.append(h_2)

            # discriminator
            logits_e, logits_i, logits_j = self.disc_layers(c, h_1, h_2, data.features, shuf_fts)
            logits_e_list.append(logits_e)
            logits_i_list.append(logits_i)
            logits_j_list.append(logits_j)

        # fusion
        h1 = self._combine_att(h_1_list)
        h2 = self._combine_att(h_2_list)
        c = torch.mean(h1, 0)   # readout
        logits_e_fusion, logits_i_fusion, logits_j_fusion = self.disc_fusion(c, h1, h2, data.features, shuf_fts)

        loss_e = loss_i = loss_j = 0
        for i in range(len(logits_e_list)):
            loss_e += self._get_loss(logits_e_list[i])
            loss_i += self._get_loss(logits_i_list[i])
            loss_j += self._get_loss(logits_j_list[i])
        # fusion
        loss_e_fusion = self._get_loss(logits_e_fusion)
        loss_i_fusion = self._get_loss(logits_i_fusion)
        loss_j_fusion = self._get_loss(logits_j_fusion)
        loss = self.args.hdmi.coef_layers[0] * loss_e + self.args.hdmi.coef_layers[1] * loss_i + self.args.hdmi.coef_layers[2] * loss_j + \
            self.args.hdmi.coef_fusion[0] * loss_e_fusion + self.args.hdmi.coef_fusion[1] * loss_i_fusion + self.args.hdmi.coef_fusion[2] * loss_j_fusion
        
        return loss
    
    def get_embedding(self, data):
        h_1_list = []
        for i, adj in enumerate(data.adj_list):
            h_1 = torch.squeeze(self.gcn_list[i](data.features, adj, self.args.dataset.sparse))
            h_1_list.append(h_1)
        h = self._combine_att(h_1_list)
        return h.detach()
        
    
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
    
    def _get_loss(self, logits):
        """
        :param logits: [2, n_nodes]
        """
        n_nodes = logits.shape[1]
        lbl_1 = torch.ones(n_nodes)
        lbl_2 = torch.zeros(n_nodes)
        lbl = torch.stack((lbl_1, lbl_2), 0)

        lbl = lbl.to(self.device)
        loss = self.criteria(logits, lbl)
        return loss

