import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random as random
import scipy.sparse as sp

from models.Heco_utils import Mp_encoder, Sc_encoder, Contrast
from utils.data_process import sparse_mx_to_torch_sparse_tensor

class Heco(nn.Module):
    def __init__(self, cfg):
        super(Heco, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.fc_list = nn.ModuleList([nn.Linear(feats_dim, cfg.gnn.hidden_dim, bias=True)
                                      for feats_dim in cfg.heco.feats_dim_list])
        if cfg.heco.feat_drop > 0:
            self.feat_drop = nn.Dropout(cfg.heco.feat_drop)
        else:
            self.feat_drop = lambda x: x
        self.mp = Mp_encoder(cfg.dataset.num_view, cfg.gnn.hidden_dim, cfg.heco.attn_drop)
        self.sc = Sc_encoder(cfg.gnn.hidden_dim, cfg.heco.sample_rate, cfg.heco.nei_num, cfg.heco.attn_drop)      
        self.contrast = Contrast(cfg.gnn.hidden_dim, cfg.heco.tau, cfg.heco.lam)
        self.init_weight()

    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0)  

    def forward(self, data):
        features = data.features
        adj_list = data.adj_list
        nei_index = data.nei_index
        pos = data.pos
        h_all = []
        for i in range(len(features)):
            h_all.append(F.elu(self.feat_drop(self.fc_list[i](features[i]))))
        z_mp = self.mp(h_all[0], adj_list)
        z_sc = self.sc(h_all, nei_index)
        loss = self.contrast(z_mp, z_sc, pos)
        return loss
    
    def get_embedding(self, data):
        z_mp = F.elu(self.fc_list[0](data.features[0]))
        z_mp = self.mp(z_mp, data.adj_list)
        return z_mp.detach()

    def preprocess(self, data):
        features = [data.features.to(self.device)]
        adj_list = [adj.to(self.device) for adj in data.adj_list]

        ### positive samples
        num_nodes = data.nb_nodes
        all = 0
        for adj in adj_list:
            adj = adj / adj.sum(axis=-1).reshape(-1,1)
            all += adj
        # all_ = (all>0).sum(-1)
        # print(all_.max(),all_.min(),all_.mean())
        pos = np.zeros((num_nodes,num_nodes))
        k=0
        for i in range(len(all)):
            one = all[i].nonzero()[0]
            if len(one) > self.args.heco.pos_num:
                oo = np.argsort(-all[i, one])
                sele = one[oo[:self.args.heco.pos_num]]
                pos[i, sele] = 1
                k+=1
            else:
                pos[i, one] = 1
        pos = sp.coo_matrix(pos)
        pos = sparse_mx_to_torch_sparse_tensor(pos).to(self.device)


        ### type-specific features
        for type_num in self.args.heco.type_num[1:]:
            features.append(torch.eye(type_num).to(self.device))


        ### nei_index
        if self.args.dataset_name == "freebase":
            nei_a = np.load("./data/freebase/raw/" + "nei_a.npy", allow_pickle=True)
            nei_d = np.load("./data/freebase/raw/" + "nei_d.npy", allow_pickle=True)
            nei_w = np.load("./data/freebase/raw/" + "nei_w.npy", allow_pickle=True)
            nei_a = [torch.LongTensor(i).to(self.device) for i in nei_a]
            nei_d = [torch.LongTensor(i).to(self.device) for i in nei_d]
            nei_w = [torch.LongTensor(i).to(self.device) for i in nei_w]
            nei_index = [nei_a, nei_d, nei_w]

        elif self.args.dataset_name == "dblp":
            nei_p = np.load("./data/dblp/raw/" + "nei_p.npy", allow_pickle=True)
            nei_p = [torch.LongTensor(i).to(self.device) for i in nei_p]
            nei_index = [nei_p,nei_p]

        data.features = features
        data.adj_list = adj_list
        data.nei_index = nei_index
        data.pos = pos
        self.args.freeze()

    def postprocess(self, data):
        pass