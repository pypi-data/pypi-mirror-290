import torch
import torch.nn as nn
import numpy as np
import random as random

from models.DMGI_utils import GCN, Discriminator, AvgReadout, Attention, LogReg


class DMGI(nn.Module):
    def __init__(self, cfg):
        super(DMGI, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.gcn = nn.ModuleList([GCN(cfg.dataset.ft_size, cfg.gnn.hidden_dim, cfg.gnn.activation, cfg.gnn.dropout, cfg.gnn.isBias) for _ in range(cfg.dataset.num_view)])
        self.disc = Discriminator(cfg.gnn.hidden_dim)
        self.H = nn.Parameter(torch.FloatTensor(cfg.dataset.nb_nodes, cfg.gnn.hidden_dim))
        self.readout_func = AvgReadout()
        self.readout_act_func = nn.Sigmoid()
        self.b_xent = nn.BCEWithLogitsLoss()
        self.xent = nn.CrossEntropyLoss()
        if cfg.dmgi.isAttn:
            self.attn = nn.ModuleList([Attention(cfg) for _ in range(cfg.dmgi.nheads)])
        if cfg.dmgi.isSemi:
            self.logistic = LogReg(cfg.gnn.hid_units, cfg.dataset.nb_classes).to(self.device)

        self.init_weight()

    def init_weight(self):
        nn.init.xavier_normal_(self.H)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0) 

    def forward(self, data):
        xent_loss = None
        idx = np.random.permutation(data.nb_nodes)
        shuf = [feature[idx, :] for feature in data.features]
        shuf = [shuf_ft.to(self.device) for shuf_ft in shuf]
        lbl_1 = torch.ones(1, data.nb_nodes)
        lbl_2 = torch.zeros(1, data.nb_nodes)
        lbl = torch.cat((lbl_1, lbl_2), 1).to(self.device)
        ######################################################################## 
        
        h_1_all = []; h_2_all = []; c_all = []; logits = []
        result = {}

        for i in range(data.num_view):
            h_1 = self.gcn[i](data.features[i], data.adj_list[i], self.args.dataset.sparse)
            # how to readout positive summary vector
            c = self.readout_func(h_1)
            c = self.readout_act_func(c)  # equation 9
            h_2 = self.gcn[i](shuf[i], data.adj_list[i], self.args.dataset.sparse)
            logit = self.disc(c, h_1, h_2, None, None)
            h_1_all.append(h_1)
            h_2_all.append(h_2)
            c_all.append(c)
            logits.append(logit)
        result['logits'] = logits

        # Attention or not
        if self.args.dmgi.isAttn:
            h_1_all_lst = []; h_2_all_lst = []; c_all_lst = []
            for h_idx in range(self.args.dmgi.nheads):
                h_1_all_, h_2_all_, c_all_ = self.attn[h_idx](h_1_all, h_2_all, c_all)
                h_1_all_lst.append(h_1_all_); h_2_all_lst.append(h_2_all_); c_all_lst.append(c_all_)
            h_1_all = torch.mean(torch.cat(h_1_all_lst, 0), 0).unsqueeze(0)
            h_2_all = torch.mean(torch.cat(h_2_all_lst, 0), 0).unsqueeze(0)
        else:
            h_1_all = torch.mean(torch.cat(h_1_all), 0).unsqueeze(0)
            h_2_all = torch.mean(torch.cat(h_2_all), 0).unsqueeze(0)

        # consensus regularizer
        pos_reg_loss = ((self.H - h_1_all) ** 2).sum()
        neg_reg_loss = ((self.H - h_2_all) ** 2).sum()
        reg_loss = pos_reg_loss - neg_reg_loss
        result['reg_loss'] = reg_loss

        # semi-supervised module
        if self.args.dmgi.isSemi:
            semi = self.logistic(self.H).squeeze(0)
            result['semi'] = semi

        ########################################################################
        logits = result['logits']
        for view_idx, logit in enumerate(logits):
            if xent_loss is None:
                xent_loss = self.b_xent(logit, lbl)
            else:
                xent_loss += self.b_xent(logit, lbl)
        loss = xent_loss

        reg_loss = result['reg_loss']
        loss += self.args.dmgi.reg_coef * reg_loss

        if self.args.dmgi.isSemi:
            sup = result['semi']
            semi_loss = self.xent(sup[data.idx_train], data.labels[data.idx_train])
            loss += self.args.dmgi.sup_coef * semi_loss

        return loss

    def get_embedding(self, data):
        return self.H.data.detach()

    def preprocess(self, data):
        features = [data.features.to(self.device) for _ in range(data.num_view)]
        data.features = features

        self.args.freeze()

    def postprocess(self, data):
        pass

