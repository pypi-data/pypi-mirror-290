import torch
import torch.nn as nn
import torch.nn.functional as F
import random as random
from torch_geometric.nn import GCNConv



class GCN(nn.Module):
    def __init__(self, cfg):
        super(GCN, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.fc_1 = nn.Linear(cfg.dataset.ft_size, cfg.gnn.hidden_dim, bias=False)
        self.fc_2 = nn.Linear(cfg.gnn.hidden_dim, cfg.dataset.nb_classes, bias=False)
        if cfg.gnn.isBias:
            self.bias_1 = nn.Parameter(torch.FloatTensor(cfg.gnn.hidden_dim))
            self.bias_1.data.fill_(0.0)
            self.bias_2 = nn.Parameter(torch.FloatTensor(cfg.dataset.nb_classes))
            self.bias_2.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)
        self.act = nn.ReLU()
        for m in self.modules():
            self.weights_init(m)
        self.drop_prob = cfg.gnn.dropout
        self.isBias = cfg.gnn.isBias
        self.sparse = cfg.dataset.sparse
        self.xent = nn.CrossEntropyLoss()  # single-label
        self.bce = nn.BCEWithLogitsLoss()  # multi-label

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    def forward(self, data):
        x = data.features
        adj_list = data.adj_list
        labels = data.labels
        idx_train = data.idx_train
        h_all = []
        for adj in adj_list:
            ### Layer 1
            seq = self.fc_1(x)
            if self.sparse:
                seq = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq, 0)), 0)
            else:
                seq = torch.bmm(adj, seq)
            if self.isBias:
                seq += self.bias_1
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            ### Layer 2
            seq = self.fc_2(seq)
            if self.sparse:
                seq = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq, 0)), 0)
            else:
                seq = torch.bmm(adj, seq)
            if self.isBias:
                seq += self.bias_2
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            h_all.append(seq)

        h_all = torch.stack(h_all, dim=0)
        h_all = torch.mean(h_all, dim=0)
        h_all = torch.squeeze(h_all)
        loss = self.xent(h_all[idx_train], labels[idx_train])
        return loss

    def get_embedding(self, data):
        x = data.features
        adj_list = data.adj_list
        h_all = []
        for adj in adj_list:
            ### Layer 1
            seq = self.fc_1(x)
            if self.sparse:
                seq = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq, 0)), 0)
            else:
                seq = torch.bmm(adj, seq)
            if self.isBias:
                seq += self.bias_1
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            ### Layer 2
            seq = self.fc_2(seq)
            if self.sparse:
                seq = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq, 0)), 0)
            else:
                seq = torch.bmm(adj, seq)
            if self.isBias:
                seq += self.bias_2
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            h_all.append(seq)

        h_all = torch.stack(h_all, dim=0)
        h_all = torch.mean(h_all, dim=0)
        h_all = torch.squeeze(h_all)

        return h_all.detach(), h_all.detach()
    
    def preprocess(self, data):
        self.args.freeze()

    def postprocess(self, data):
        pass


'''
### Using PyG's Implementation could cause OOM error, should add multi-GPU in the future...
class GCN(nn.Module):
    def __init__(self, cfg):
        super(GCN, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.conv1 = GCNConv(cfg.dataset.ft_size, cfg.gnn.hidden_dim)
        self.conv2 = GCNConv(cfg.gnn.hidden_dim, cfg.dataset.nb_classes)
        self.dropout = cfg.gnn.dropout
        self.xent = nn.CrossEntropyLoss()


    def forward(self, data):
        x = data.features
        edge_index_list = data.edge_index_list
        labels = data.labels
        idx_train = data.idx_train
        h_all = []
        for edge_index in edge_index_list:
            h = self.conv1(x, edge_index)
            h = F.relu(h)
            h = F.dropout(h, p=self.dropout, training=self.training)
            h = self.conv2(h, edge_index)
            h_all.append(h)

        h_all = torch.stack(h_all, dim=0)
        h_all = torch.mean(h_all, dim=0)
        loss = self.xent(h_all[idx_train], labels[idx_train])
        return loss

    def get_embedding(self, data):
        x = data.features
        edge_index_list = data.edge_index_list
        h_all = []
        for edge_index in edge_index_list:
            h = self.conv1(x, edge_index)
            h = F.relu(h)
            h = F.dropout(h, p=self.dropout, training=self.training)
            h = self.conv2(h, edge_index)
            h_all.append(h)

        h_all = torch.stack(h_all, dim=0)
        h_all = torch.mean(h_all, dim=0)
        return h_all.detach(), h_all.detach()
    
    def preprocess(self, data):
        self.args.freeze()

    def postprocess(self, data):
        pass
'''