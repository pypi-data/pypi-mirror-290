import torch
import torch.nn as nn
import torch.nn.functional as F
import random as random
from torch_geometric.nn import GATConv



class GATLayer(nn.Module):
    def __init__(self, in_features, out_features, dropout, alpha, concat=True):
        super(GATLayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha
        self.concat = concat

        self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
        nn.init.xavier_uniform_(self.W.data)

        self.a = nn.Parameter(torch.zeros(size=(2*out_features, 1)))
        nn.init.xavier_uniform_(self.a.data)

        self.dropout = nn.Dropout(dropout)
        self.leakyrelu = nn.LeakyReLU(self.alpha)

    def forward(self, h, adj):
        Wh = torch.mm(h, self.W)
        a_input = self._prepare_attentional_mechanism_input(Wh)
        e = self.leakyrelu(torch.matmul(a_input, self.a).squeeze(2))

        zero_vec = -9e15 * torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)

        attention = F.softmax(attention, dim=1)
        attention = self.dropout(attention)

        h_prime = torch.matmul(attention, Wh)

        if self.concat:
            return F.elu(h_prime)
        else:
            return h_prime

    def _prepare_attentional_mechanism_input(self, Wh):
        N = Wh.size()[0]

        Wh_repeated_in_chunks = Wh.repeat_interleave(N, dim=0)
        Wh_repeated_alternating = Wh.repeat(N, 1)

        all_combinations_matrix = torch.cat([Wh_repeated_in_chunks, Wh_repeated_alternating], dim=1)

        return all_combinations_matrix.view(N, -1, 2 * self.out_features)

class GAT(nn.Module):
    def __init__(self, cfg):
        super(GAT, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.fc_1 = GATLayer(cfg.dataset.ft_size, cfg.dataset.nb_classes, cfg.gnn.dropout, alpha=0.2, concat=True)
        self.fc_2 = GATLayer(cfg.gnn.hidden_dim, cfg.dataset.nb_classes, cfg.gnn.dropout, alpha=0.2, concat=True)
        if cfg.gnn.isBias:
            self.bias_1 = nn.Parameter(torch.FloatTensor(cfg.dataset.nb_classes))
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
            torch.nn.init.xavier_uniform_(m.W.data)
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
            seq = self.fc_1(x, adj)
            if self.isBias:
                seq += self.bias_1
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            # ### Layer 2
            # seq = self.fc_2(seq, adj)
            # if self.isBias:
            #     seq += self.bias_2
            # seq = self.act(seq)
            # seq = F.dropout(seq, self.drop_prob, training=self.training)

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
            seq = self.fc_1(x, adj)
            if self.isBias:
                seq += self.bias_1
            seq = self.act(seq)
            seq = F.dropout(seq, self.drop_prob, training=self.training)

            # ### Layer 2
            # seq = self.fc_2(seq, adj)
            # if self.isBias:
            #     seq += self.bias_2
            # seq = self.act(seq)
            # seq = F.dropout(seq, self.drop_prob, training=self.training)

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
class GAT(nn.Module):
    def __init__(self, cfg):
        super(GAT, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.conv1 = GATConv(cfg.dataset.ft_size, cfg.gnn.hidden_dim)
        self.conv2 = GATConv(cfg.gnn.hidden_dim, cfg.dataset.nb_classes)
        self.criterion = nn.CrossEntropyLoss()


    def forward(self, data):
        x = data.features
        edge_index_list = data.edge_index_list
        labels = data.labels
        idx_train = data.idx_train
        h_all = []
        for edge_index in edge_index_list:
            h = self.conv1(x, edge_index)
            h = F.relu(h)
            h = F.dropout(h, training=self.training)
            h = self.conv2(h, edge_index)
            h_all.append(h)

        h_all = torch.stack(h_all, dim=0)
        h_all = torch.mean(h_all, dim=0)
        loss = self.criterion(h_all[idx_train], labels[idx_train])
        return loss

    def get_embedding(self, data):
        x = data.features
        edge_index_list = data.edge_index_list
        labels = data.labels
        h_all = []
        for edge_index in edge_index_list:
            h = self.conv1(x, edge_index)
            h = F.relu(h)
            h = F.dropout(h, training=self.training)
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