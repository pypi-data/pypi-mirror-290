import torch
import torch.nn as nn
import torch.nn.functional as F


class HANLayer(nn.Module):
    def __init__(self, in_features, out_features, dropout, alpha, concat=True):
        super(HANLayer, self).__init__()
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
    

class Attention(nn.Module):
    def __init__(self, cfg):
        super(Attention, self).__init__()
        self.args = cfg
        self.A = nn.ModuleList([nn.Linear(cfg.dataset.nb_classes, 1) for _ in range(cfg.dataset.num_view)])
        self.weight_init()

    def weight_init(self):
        for i in range(self.args.dataset.num_view):
            nn.init.xavier_normal_(self.A[i].weight)
            self.A[i].bias.data.fill_(0.0)

    def forward(self, feat_pos):
        feat_pos, feat_pos_attn = self.attn_feature(feat_pos)
        return feat_pos.squeeze()

    def attn_feature(self, features):
        features_attn = []
        for i in range(self.args.dataset.num_view):
            features_attn.append((self.A[i](features[i].squeeze())))
        features_attn = F.softmax(torch.cat(features_attn, 1), -1)
        features = torch.cat(features,1).squeeze(0)
        features_attn_reshaped = features_attn.transpose(1, 0).contiguous().view(-1, 1)
        features = features * features_attn_reshaped.expand_as(features)
        features = features.view(self.args.dataset.num_view, self.args.dataset.nb_nodes, self.args.dataset.nb_classes).sum(0).unsqueeze(0)
        return features, features_attn
    