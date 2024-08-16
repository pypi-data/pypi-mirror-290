import torch
import torch.nn as nn
import torch.nn.functional as F
import random as random
from typing import Any, Optional, Tuple


#######################################################################
# GNNDAE-related
class GCN(nn.Module):
    def __init__(self, in_ft, out_ft, act, drop_prob, isBias=False):
        super(GCN, self).__init__()
        self.fc_1 = nn.Linear(in_ft, out_ft, bias=False)
        if act == 'prelu':
            self.act = nn.PReLU()
        elif act == 'relu':
            self.act = nn.ReLU()
        if isBias:
            self.bias_1 = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias_1.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)
        for m in self.modules():
            self.weights_init(m)
        self.drop_prob = drop_prob
        self.isBias = isBias

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    # Shape of seq: (batch, nodes, features)
    def forward(self, seq, adj, sparse=False):
        seq = F.dropout(seq, self.drop_prob, training=self.training)
        seq_raw = self.fc_1(seq)
        if sparse:
            seq = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq_raw, 0)), 0)
        else:
            seq = torch.mm(adj, seq_raw)
        if self.isBias:
            seq += self.bias_1
        return self.act(seq)


class GNNEncoder(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.pipe = GCN(cfg.dataset.ft_size, cfg.gnn.hidden_dim, cfg.gnn.activation, cfg.gnn.dropout, cfg.gnn.isBias)
        # map to common
        self.S = nn.Linear(cfg.gnn.hidden_dim, cfg.dmg.c_dim)
        # map to private
        self.P = nn.Linear(cfg.gnn.hidden_dim, cfg.dmg.p_dim)

    def forward(self, x, adj):
        tmp = self.pipe(x, adj)
        common = self.S(tmp)
        private = self.P(tmp)
        return common, private


class Linearlayer(nn.Module):
    def __init__(self, num_layers, input_dim, hidden_dim, output_dim):
        super(Linearlayer, self).__init__()
        self.linear_or_not = True  # default is linear model
        self.num_layers = num_layers
        if num_layers < 1:
            raise ValueError("number of layers should be positive!")
        elif num_layers == 1:
            # Linear model
            self.linear = nn.Linear(input_dim, output_dim)
        else:
            # Multi-layer model
            self.linear_or_not = False
            self.linears = torch.nn.ModuleList()
            self.batch_norms = torch.nn.ModuleList()
            self.linears.append(nn.Linear(input_dim, hidden_dim))
            for layer in range(num_layers - 2):
                self.linears.append(nn.Linear(hidden_dim, hidden_dim))
            self.linears.append(nn.Linear(hidden_dim, output_dim))
            for layer in range(num_layers - 1):
                self.batch_norms.append(nn.BatchNorm1d((hidden_dim)))

    def forward(self, x):
        if self.linear_or_not:
            # If linear model
            return self.linear(x)
        else:
            # If MLP
            h = x
            for layer in range(self.num_layers - 1):
                h = F.relu(self.batch_norms[layer](self.linears[layer](h)))
            return self.linears[self.num_layers - 1](h)


class Decoder(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        # self.args = args
        self.linear1 = Linearlayer(cfg.dmg.decolayer, cfg.dmg.c_dim+cfg.dmg.p_dim, cfg.gnn.hidden_dim, cfg.dataset.ft_size)
        self.linear2 = nn.Linear(cfg.dataset.ft_size, cfg.dataset.ft_size)

    def forward(self, s, p):
        recons = self.linear1(torch.cat((s, p), 1))
        recons = self.linear2(F.relu(recons))
        return recons


class GNNDAE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.num_view = cfg.dataset.num_view
        self.encoder = nn.ModuleList()
        self.decoder = nn.ModuleList()
        for _ in range(self.num_view):
            self.encoder.append(GNNEncoder(cfg))
            self.decoder.append(Decoder(cfg))

    def encode(self, x, adj_list):
        common = []
        private = []
        for i in range(self.num_view):
            tmp = self.encoder[i](x[i], adj_list[i])
            common.append(tmp[0])
            private.append(tmp[1])
        return common, private

    def decode(self, s, p):
        recons = []
        for i in range(self.num_view):
            tmp = self.decoder[i](s[i], p[i])
            recons.append(tmp)
        return recons

    def forward(self, x, adj):
        common, private = self.encode(x, adj)
        recons = self.decode(common, private)
        return common, private, recons

    def embed(self, x, adj_list):
        common = []
        private = []
        for i in range(self.num_view):
            tmp = self.encoder[i](x[i], adj_list[i])
            common.append(tmp[0].detach())
            private.append(tmp[1].detach())
        return common, private
#######################################################################




#######################################################################
# MeasureF-related
class GradientReversalLayer(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Any, input: torch.Tensor, coeff: Optional[float] = 1.) -> torch.Tensor:
        ctx.coeff = coeff
        output = input * 1.0
        return output
    @staticmethod
    def backward(ctx: Any, grad_output: torch.Tensor) -> Tuple[torch.Tensor, Any]:
        return grad_output.neg() * ctx.coeff, None

def grad_reverse(x, coeff):
    return GradientReversalLayer.apply(x, coeff)


class MLP(nn.Module):
    def __init__(self, input_d, structure, output_d, dropprob=0.0):
        super(MLP, self).__init__()
        self.net = nn.ModuleList()
        self.dropout = torch.nn.Dropout(dropprob)
        struc = [input_d] + structure + [output_d]
        for i in range(len(struc)-1):
            self.net.append(nn.Linear(struc[i], struc[i+1]))

    def forward(self, x):
        for i in range(len(self.net)-1):
            x = F.relu(self.net[i](x))
            x = self.dropout(x)
        # For the last layer
        y = self.net[-1](x)
        return y

class Measure_F(nn.Module):
    def __init__(self, view1_dim, view2_dim, phi_size, psi_size, latent_dim=1):
        super(Measure_F, self).__init__()
        self.phi = MLP(view1_dim, phi_size, latent_dim)
        self.psi = MLP(view2_dim, psi_size, latent_dim)
        # gradient reversal layer
        self.grl1 = GradientReversalLayer()
        self.grl2 = GradientReversalLayer()

    def forward(self, x1, x2):
        y1 = self.phi(grad_reverse(x1,1))
        y2 = self.psi(grad_reverse(x2,1))
        return y1, y2
#######################################################################


def drop_feature(x, drop_prob):
    drop_mask = torch.empty(
        (x.size(1),),
        dtype=torch.float32,
        device=x.device).uniform_(0, 1) < drop_prob
    x = x.clone()
    x[:, drop_mask] = 0
    return x
