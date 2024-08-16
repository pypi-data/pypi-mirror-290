import torch
import torch.nn as nn
import torch.nn.functional as F

from models.HAN_utils import HANLayer, Attention


class HAN(nn.Module):
    def __init__(self, cfg):
        super(HAN, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        # Define HAN layer for each edge type
        self.num_edge_types = cfg.dataset.num_view
        self.layers = nn.ModuleList([HANLayer(cfg.dataset.ft_size, cfg.dataset.nb_classes, cfg.gnn.dropout, alpha=0.2, concat=True) for _ in range(self.num_edge_types)])
        self.attn = Attention(cfg)
        self.act = nn.ReLU()
        if cfg.gnn.isBias:
            self.bias_1 = nn.Parameter(torch.FloatTensor(cfg.dataset.nb_classes))
            self.bias_1.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)
        # for m in self.modules():
        #     self.weights_init(m)
        self.drop_prob = cfg.gnn.dropout
        self.isBias = cfg.gnn.isBias
        self.xent = nn.CrossEntropyLoss()
        self.bce = nn.BCEWithLogitsLoss()

    # def weights_init(self, m):
    #     if isinstance(m, nn.Linear):
    #         torch.nn.init.xavier_uniform_(m.W.data)
    #         if m.bias is not None:
    #             m.bias.data.fill_(0.0)

    def forward(self, data):
        x = data.features
        adj_list = data.adj_list
        labels = data.labels
        idx_train = data.idx_train

        h_all = []
        for i, adj in enumerate(adj_list):
            # HAN layer for each edge type
            h_i = self.layers[i](x, adj)
            h_all.append(h_i.unsqueeze(0))
            
        h_all = self.attn(h_all)
        loss = self.xent(h_all[idx_train], labels[idx_train])
        return loss

    def get_embedding(self, data):
        x = data.features
        adj_list = data.adj_list

        h_all = []
        for i, adj in enumerate(adj_list):
            # HAN layer for each edge type
            h_i = self.layers[i](x, adj)
            h_all.append(h_i.unsqueeze(0))

        h_all = self.attn(h_all)
        return h_all.detach(), h_all.detach()

    def preprocess(self, data):
        self.args.freeze()

    def postprocess(self, data):
        pass
