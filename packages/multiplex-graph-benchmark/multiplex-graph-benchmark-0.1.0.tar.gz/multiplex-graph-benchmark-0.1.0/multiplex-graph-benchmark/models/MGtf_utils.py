import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, SAGEConv
import math

class MLP(nn.Module):
    def __init__(self, input_d, structure, output_d, dropprob=0.0):
        super(MLP, self).__init__()
        self.net = nn.ModuleList()
        self.norms = nn.ModuleList()
        self.dropout = nn.Dropout(dropprob)
        struc = [input_d] + structure + [output_d]

        for i in range(len(struc)-1):
            self.net.append(nn.Linear(struc[i], struc[i+1]))
            self.norms.append(nn.BatchNorm1d(struc[i+1]))

    def forward(self, x):
        for i in range(len(self.net)-1):
            x = F.relu(self.net[i](x))
            # x = F.relu(self.norms[i](self.net[i](x)))
            x = self.dropout(x)

        y = self.net[-1](x)
        return F.softmax(y, dim=1)



class GNN(nn.Module):
    def __init__(self, input_dim, d_model, conv='GAT', dropout_prob=0.1):
        super().__init__()
        if conv == 'SAGE':
            self.conv1 = SAGEConv(input_dim, d_model)
            self.conv2 = SAGEConv(d_model, d_model)
        elif conv == 'GCN':
            self.conv1 = GCNConv(input_dim, d_model)
            self.conv2 = GCNConv(d_model, d_model)
        elif conv == 'GAT':
            self.conv1 = GATConv(input_dim, d_model, heads=2)
            self.conv2 = GATConv(d_model * 2, d_model, heads=2)
        else:
            raise ValueError(f"Unsupported convolution type: {conv}")
        
        self.dropout = nn.Dropout(p=dropout_prob)

    def forward(self, x, edge_index):
        x = F.elu(self.conv1(x, edge_index))
        x = self.dropout(x) 
        x = self.conv2(x, edge_index)

        return x



class PositionalEncoding(nn.Module):
    """
    compute sinusoid encoding.
    """
    def __init__(self, d_model, max_len, device):
        """
        constructor of sinusoid encoding class

        :param d_model: dimension of model
        :param max_len: max sequence length
        :param device: hardware device setting
        """
        super(PositionalEncoding, self).__init__()

        # same size with input matrix (for adding with input matrix)
        self.encoding = torch.zeros(max_len, d_model, device=device)
        self.encoding.requires_grad = False  # we don't need to compute gradient

        pos = torch.arange(0, max_len, device=device)
        pos = pos.float().unsqueeze(dim=1)
        # 1D => 2D unsqueeze to represent word's position

        _2i = torch.arange(0, d_model, step=2, device=device).float()
        # 'i' means index of d_model (e.g. embedding size = 50, 'i' = [0,50])
        # "step=2" means 'i' multiplied with two (same with 2 * i)

        self.encoding[:, 0::2] = torch.sin(pos / (10000 ** (_2i / d_model)))
        self.encoding[:, 1::2] = torch.cos(pos / (10000 ** (_2i / d_model)))
        # compute positional encoding to consider positional information of words

    def forward(self, x):
        # self.encoding
        # [max_len = 512, d_model = 512]

        batch_size, seq_len = x.size()
        # [batch_size = 128, seq_len = 30]

        return self.encoding[:seq_len, :]
        # [seq_len = 30, d_model = 512]
        # it will add with tok_emb : [128, 30, 512]         


class MultiHeadAttention(nn.Module):

    def __init__(self, d_model, n_head):
        super(MultiHeadAttention, self).__init__()
        self.n_head = n_head
        self.attention = ScaleDotProductAttention()
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_concat = nn.Linear(d_model, d_model)

    def forward(self, q, k, v, bias=None, mask=None):
        # 1. dot product with weight matrices
        q, k, v = self.w_q(q), self.w_k(k), self.w_v(v)

        # 2. split tensor by number of heads
        q, k, v = self.split(q), self.split(k), self.split(v)

        if bias is not None:
            bias = bias.unsqueeze(1)
            bias = bias.expand(-1, self.n_head, -1, -1)

        if mask is not None:
            mask = mask.unsqueeze(1).unsqueeze(2)
            mask = mask.expand(-1, self.n_head, -1, -1)

        # 3. do scale dot product to compute similarity
        out, attention = self.attention(q, k, v, bias=bias, mask=mask)
        
        # 4. concat and pass to linear layer
        out = self.concat(out)
        out = self.w_concat(out)

        # 5. visualize attention map
        # TODO : we should implement visualization

        return out

    def split(self, tensor):
        """
        split tensor by number of head

        :param tensor: [batch_size, length, d_model]
        :return: [batch_size, head, length, d_tensor]
        """
        batch_size, length, d_model = tensor.size()

        d_tensor = d_model // self.n_head
        tensor = tensor.view(batch_size, length, self.n_head, d_tensor).transpose(1, 2)
        # it is similar with group convolution (split by number of heads)

        return tensor

    def concat(self, tensor):
        """
        inverse function of self.split(tensor : torch.Tensor)

        :param tensor: [batch_size, head, length, d_tensor]
        :return: [batch_size, length, d_model]
        """
        batch_size, head, length, d_tensor = tensor.size()
        d_model = head * d_tensor

        tensor = tensor.transpose(1, 2).contiguous().view(batch_size, length, d_model)
        return tensor


class ScaleDotProductAttention(nn.Module):
    """
    compute scale dot product attention

    Query : given sentence that we focused on (decoder)
    Key : every sentence to check relationship with Qeury(encoder)
    Value : every sentence same with Key (encoder)
    """

    def __init__(self):
        super(ScaleDotProductAttention, self).__init__()
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, q, k, v, bias=None, mask=None, e=1e-12):
        # input is 4 dimension tensor
        # [batch_size, head, length, d_tensor]
        batch_size, head, length, d_tensor = k.size()

        # 1. dot product Query with Key^T to compute similarity
        k_t = k.transpose(2, 3)  # transpose
        score = (q @ k_t) / math.sqrt(d_tensor)  # scaled dot product

        if bias is not None:
            score = score * bias
            # score = score + bias

        # 2. apply masking (opt)
        if mask is not None:
            score = score.masked_fill(mask == 0, -10000)

        # 3. pass them softmax to make [0, 1] range
        score = self.softmax(score)

        # 4. multiply with Value
        v = score @ v

        return v, score
class LayerNorm(nn.Module):
    def __init__(self, d_model, eps=1e-12):
        super(LayerNorm, self).__init__()
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta = nn.Parameter(torch.zeros(d_model))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        var = x.var(-1, unbiased=False, keepdim=True)
        # '-1' means last dimension. 

        out = (x - mean) / torch.sqrt(var + self.eps)
        out = self.gamma * out + self.beta
        return out


class PositionwiseFeedForward(nn.Module):

    def __init__(self, d_model, hidden, drop_prob=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.linear1 = nn.Linear(d_model, hidden)
        self.linear2 = nn.Linear(hidden, d_model)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=drop_prob)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x


class EncoderLayer(nn.Module):
    def __init__(self, d_model, ffn_hidden, n_head, drop_prob):
        super(EncoderLayer, self).__init__()
        self.attention = MultiHeadAttention(d_model=d_model, n_head=n_head)
        self.norm1 = LayerNorm(d_model=d_model)
        self.dropout1 = nn.Dropout(p=drop_prob)

        self.ffn = PositionwiseFeedForward(d_model=d_model, hidden=ffn_hidden, drop_prob=drop_prob)
        self.norm2 = LayerNorm(d_model=d_model)
        self.dropout2 = nn.Dropout(p=drop_prob)

    def forward(self, x, attn, src_mask):
        # 1. compute self attention
        _x = x
        x = self.attention(q=x, k=x, v=x, bias=attn, mask=src_mask)
        
        # 2. add and norm
        x = self.dropout1(x)
        x = self.norm1(x + _x)
        
        # 3. positionwise feed forward network
        _x = x
        x = self.ffn(x)
      
        # 4. add and norm
        x = self.dropout2(x)
        x = self.norm2(x + _x)
        return x


class TransformerEncoder(nn.Module):
    def __init__(self, input_dim, d_model, ffn_hidden, n_head, n_layers, drop_prob):
        super().__init__()
        # self.emb = TransformerEmbedding(d_model=d_model,
        #                                 max_len=max_len,
        #                                 vocab_size=enc_voc_size,
        #                                 drop_prob=drop_prob,
        #                                 device=device)
        self.emb = nn.Sequential(nn.Linear(input_dim, d_model), nn.ReLU())

        self.layers = nn.ModuleList([EncoderLayer(d_model=d_model,
                                                  ffn_hidden=ffn_hidden,
                                                  n_head=n_head,
                                                  drop_prob=drop_prob)
                                     for _ in range(n_layers)])
        
        # self.dummy_node = nn.Parameter(torch.randn(1, 1, d_model))  # Initialize a learnable dummy node

    def forward(self, x, attn=None, src_mask=None):
        # batch_size, seq_length, dim = x.size()
        # dummy_nodes = self.dummy_node.expand(batch_size, 1, dim)
        # x = torch.cat([dummy_nodes, x], dim=1)

        # in case used as aggregator
        if isinstance(x, list):
            x = torch.stack(x, dim=0).permute(1,0,2)

        x = self.emb(x)

        for layer in self.layers:
            x = layer(x, attn, src_mask)

        return x[:,0,:]
    


'''
class AttentionAggregator(nn.Module):
    def __init__(self, input_dim):
        super(AttentionAggregator, self).__init__()
        self.attention_weights = nn.Linear(input_dim, 1)
        
    def forward(self, input_tensor):
        # Calculate attention weights for each view
        input_tensor = torch.stack(input_tensor, dim=0).permute(1,0,2)
        attention_scores = self.attention_weights(input_tensor)
        attention_scores = torch.softmax(attention_scores, dim=1)  # Apply softmax along num_views
        
        # Weighted sum of views
        weighted_views = torch.sum(input_tensor * attention_scores, dim=1)
        
        return weighted_views
'''

class MeanAggregator(nn.Module):
    def __init__(self):
        super(MeanAggregator, self).__init__()

    def forward(self, input_tensor):
        return torch.stack(input_tensor, dim=0).mean(dim=0)
    

class ConcatAggregator(nn.Module):
    def __init__(self):
        super(ConcatAggregator, self).__init__()

    def forward(self, input_tensor):
        return torch.cat(input_tensor, dim=-1)


class AttentionAggregator(nn.Module):
    def __init__(self, input_dim, layers):
        super(AttentionAggregator, self).__init__()
        self.w_list = nn.ModuleList([nn.Linear(input_dim, input_dim, bias=True) for _ in range(layers)])
        self.y_list = nn.ModuleList([nn.Linear(input_dim, 1) for _ in range(layers)])  #should pre-compute!!

    def forward(self, h_list):
        # input_tensor shape: [layers, batch_size, dim]
        h_combine_list = []
        for i, h in enumerate(h_list):
            h = self.w_list[i](h)
            h = self.y_list[i](h)
            h_combine_list.append(h)
        score = torch.cat(h_combine_list, -1)  
        score = torch.tanh(score)

        score = F.softmax(score, dim=-1)
        score = torch.unsqueeze(score, -1)
        h = torch.stack(h_list, dim=1)

        h = score * h
        h = torch.sum(h, dim=1)
        h = torch.squeeze(h)
        return h


AGGRCODINGS = {
    'mean': MeanAggregator,
    'concat': ConcatAggregator,
    'attn': AttentionAggregator,
    'transformer': TransformerEncoder,
}