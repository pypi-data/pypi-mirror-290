import torch
from torch import Tensor
import torch.nn as nn
from torch.utils.data import DataLoader

from torch_geometric.utils import sort_edge_index
from torch_geometric.utils.sparse import index2ptr
from torch_cluster import random_walk  # Import random_walk from torch_cluster


class MNE(nn.Module):
    def __init__(self, cfg):
        super(MNE, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.random_walk_fn = random_walk
        self.EPS = 1e-15
        assert cfg.mne.walk_length >= cfg.mne.context_size
        self.embedding_dim = cfg.dataset.ft_size
        self.walk_length = cfg.mne.walk_length - 1
        self.context_size = cfg.mne.context_size
        self.walks_per_node = cfg.mne.walks_per_node
        self.p = cfg.mne.p
        self.q = cfg.mne.q
        self.num_negative_samples = cfg.mne.num_negative_samples
        self.num_nodes = cfg.dataset.nb_nodes
        self.num_view = cfg.dataset.num_view

        self.embedding_common = nn.Parameter(torch.zeros(self.num_nodes, self.embedding_dim))
        self.embedding_privates = nn.ParameterList([
            nn.Parameter(torch.zeros(self.num_nodes, self.embedding_dim)) for _ in range(self.num_view)
        ])
        self.embedding_privates_W = nn.ModuleList([
            nn.Linear(self.embedding_dim, self.embedding_dim) for _ in range(self.num_view)
        ])
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.embedding_common)
        for i in range(self.num_view):
            nn.init.xavier_uniform_(self.embedding_privates[i])
            nn.init.xavier_uniform_(self.embedding_privates_W[i].weight)
            if self.embedding_privates_W[i].bias is not None:
                nn.init.zeros_(self.embedding_privates_W[i].bias)

    def forward(self, data):
        total_loss = 0.0
        edge_index_list = data.edge_index_list
        for edge_index in edge_index_list:
            loss = 0.0
            row, col = sort_edge_index(edge_index, num_nodes=self.num_nodes).cpu()
            self.row = row
            self.col = col
            loader = self.loader(batch_size=128, shuffle=True, num_workers=4)
            for pos_rw, neg_rw in loader:
                loss += self.loss(pos_rw.to(self.device), neg_rw.to(self.device))
            loss = loss / len(loader)
            total_loss += loss
        total_loss = total_loss / (data.num_view)
        return total_loss

    def get_embedding(self, data=None):
        common_embeddings = self.embedding_common
        relation_embeddings = [
            W(self.embedding_privates[i])
            for i, W in enumerate(self.embedding_privates_W)
        ]
        embeddings = [common_embeddings + emb for emb in relation_embeddings]
        return torch.stack(embeddings).mean(dim=0).detach()

    def preprocess(self, data):
        self.embedding_common.data.copy_(data.features)
        for i in range(self.num_view):
            self.embedding_privates[i].data.copy_(data.features)
        self.args.freeze()

    def postprocess(self, data):
        pass

    def loader(self, **kwargs):
        return DataLoader(range(self.num_nodes), collate_fn=self.sample, **kwargs)

    @torch.jit.export
    def sample(self, batch):
        if not isinstance(batch, Tensor):
            batch = torch.tensor(batch)
        return self.pos_sample(batch), self.neg_sample(batch)

    @torch.jit.export
    def pos_sample(self, batch):
        batch = batch.repeat(self.walks_per_node)
        rw = self.random_walk_fn(self.row, self.col, batch, self.walk_length, self.p, self.q)
        if not isinstance(rw, Tensor):
            rw = rw[0]
        walks = []
        num_walks_per_rw = 1 + self.walk_length + 1 - self.context_size
        for j in range(num_walks_per_rw):
            walks.append(rw[:, j:j + self.context_size])
        return torch.cat(walks, dim=0)

    @torch.jit.export
    def neg_sample(self, batch):
        batch = batch.repeat(self.walks_per_node * self.num_negative_samples)
        rw = torch.randint(self.num_nodes, (batch.size(0), self.walk_length), dtype=batch.dtype, device=batch.device)
        rw = torch.cat([batch.view(-1, 1), rw], dim=-1)
        walks = []
        num_walks_per_rw = 1 + self.walk_length + 1 - self.context_size
        for j in range(num_walks_per_rw):
            walks.append(rw[:, j:j + self.context_size])
        return torch.cat(walks, dim=0)

    def loss(self, pos_rw, neg_rw):
        embedding = self.embedding_common.data
        for private_i, W_i in zip(self.embedding_privates, self.embedding_privates_W):
            embedding = embedding + W_i(private_i.data)
        embedding = nn.Embedding.from_pretrained(embedding, freeze=False)

        # Positive loss.
        start, rest = pos_rw[:, 0], pos_rw[:, 1:].contiguous()
        h_start = embedding(start).view(pos_rw.size(0), 1, self.embedding_dim)
        h_rest = embedding(rest.view(-1)).view(pos_rw.size(0), -1, self.embedding_dim)
        out = (h_start * h_rest).sum(dim=-1).view(-1)
        pos_loss = -torch.log(torch.sigmoid(out) + self.EPS).mean()

        # Negative loss.
        start, rest = neg_rw[:, 0], neg_rw[:, 1:].contiguous()
        h_start = embedding(start).view(neg_rw.size(0), 1, self.embedding_dim)
        h_rest = embedding(rest.view(-1)).view(neg_rw.size(0), -1, self.embedding_dim)
        out = (h_start * h_rest).sum(dim=-1).view(-1)
        neg_loss = -torch.log(1 - torch.sigmoid(out) + self.EPS).mean()

        return pos_loss + neg_loss
