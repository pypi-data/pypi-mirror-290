import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.utils import degree
import numpy as np
import random as random

from models.DMG_utils import GNNDAE, Measure_F, drop_feature


class DMG(nn.Module):
    def __init__(self, cfg):
        super(DMG, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.ae_model = GNNDAE(cfg)
        self.mea_func = nn.ModuleList([Measure_F(cfg.dmg.c_dim, cfg.dmg.p_dim, 
                                                [cfg.dmg.phi_hidden_size] * cfg.dmg.phi_num_layers,
                                                [cfg.dmg.phi_hidden_size] * cfg.dmg.phi_num_layers) for _ in range(cfg.dataset.num_view)])

        self.criteria = nn.BCEWithLogitsLoss()
        self.sigm = nn.Sigmoid()
        self.log_sigmoid = nn.LogSigmoid()


        self.init_weight()

    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0) 

    def forward(self, data, optimizer, epoch):
        U = self._update_S(self.ae_model, data.features, data.adj_list, self.args.dmg.c_dim)
        for innerepoch in range(self.args.dmg.inner_epochs):
            optimizer.zero_grad()
            common, private, recons = self.ae_model(data.features, data.adj_list)
            match_loss, recons_loss = self._loss_matching_recons(common, recons, data.features, U, data.idx_p_list, epoch*innerepoch)
            phi_c_list = []
            psi_p_list = []
            for i in range(self.args.dataset.num_view):
                phi_c, psi_p = self.mea_func[i](common[i], private[i])
                phi_c_list.append(phi_c)
                psi_p_list.append(psi_p)
            cor_loss = self._loss_independence(phi_c_list, psi_p_list)
            con_loss = self._loss_contrastive(U, private, data.adj_list)
            loss = match_loss + self.args.dmg.alpha*(recons_loss) - self.args.dmg.beta*cor_loss + self.args.dmg.lammbda*con_loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.parameters(), 5.0)
            optimizer.step()
        return loss
    

    def get_embedding(self, data):
        self.ae_model.eval()
        embedding = []
        hf = self._update_S(self.ae_model, data.features, data.adj_list, self.args.dmg.c_dim)
        _, private = self.ae_model.embed(data.features, data.adj_list)
        private = sum(private) / self.args.dataset.num_view
        embedding.append(hf)
        embedding.append(private)
        embeddings = torch.cat(embedding,1)
        return embeddings

    def preprocess(self, data):
        idx_p_list = []
        sample_edge_list = []
        for adj in data.adj_list:
            deg_list_0 = []
            idx_p_list_0 = []
            deg_list_0.append(0)
            if self.args.dataset.sparse:
                A_degree = degree(adj._indices()[0], data.features.shape[0], dtype=int).tolist()
                out_node = adj._indices()[1]
            else:
                A_degree = degree(adj.to_sparse()._indices()[0], data.features.shape[0], dtype=int).tolist()
                out_node = adj.to_sparse()._indices()[1]
            for i in range(data.features.shape[0]):  
                deg_list_0.append(deg_list_0[-1] + A_degree[i])
            for j in range(1, self.args.dmg.neighbor_num+1):
                random_list = [deg_list_0[i] + j % A_degree[i] for i in range(data.features.shape[0])]
                idx_p_0 = out_node[random_list]
                idx_p_list_0.append(idx_p_0)
            idx_p_list.append(idx_p_list_0)

        features = [drop_feature(data.features, self.args.dmg.feature_drop).to(self.device) for _ in range(self.args.dataset.num_view)]
        adj_list = [adj.to(self.device) for adj in data.adj_list]

        data.idx_p_list = idx_p_list
        data.sample_edge_list = sample_edge_list
        data.features = features
        data.adj_list = adj_list

    def postprocess(self, data):
        pass

    def _update_S(self, model, features, adj_list, c_dim):
        model.eval()
        FF = []
        with torch.no_grad():
            # Forward
            common, _ = model.encode(features, adj_list)
            FF.append(torch.cat(common, 1))

            FF = torch.cat(FF, 0)

            # The projection step, i.e., subtract the mean
            FF = FF - torch.mean(FF, 0, True)

            h=[]
            for i in range(2):
                h.append(FF[:,i*c_dim:(i+1)*c_dim])

            FF = torch.stack(h, dim=2)

            # The SVD step
            U, _, T = torch.svd(torch.sum(FF, dim=2).to('cpu'))
            S = torch.mm(U, T.t())
            S = S*(FF.shape[0])**0.5
        return S.to(FF.device)

    # The loss function for matching and reconstruction
    def _loss_matching_recons(self, s, x_hat, x, U_batch, idx_p_list, epoch):
        l = torch.nn.MSELoss(reduction='sum')

        # Matching loss
        match_err = l(torch.cat(s, 1), U_batch.repeat(1, self.args.dataset.num_view))/s[0].shape[0]

        # Feature reconstruction loss
        recons_err = 0
        for i in range(self.args.dataset.num_view):
            recons_err += l(x_hat[i], x[i])
        recons_err /= s[0].shape[0]

        # Topology reconstruction loss
        interval = int(self.args.dmg.neighbor_num/self.args.dmg.sample_neighbor)
        neighbor_embedding = []
        for i in range(self.args.dataset.num_view):
            neighbor_embedding_0 = []
            for j in range(0, self.args.dmg.sample_neighbor+1):
                neighbor_embedding_0.append(x[i][idx_p_list[i][(epoch + interval * j) % self.args.dmg.neighbor_num]])
            neighbor_embedding.append(sum(neighbor_embedding_0) / self.args.dmg.sample_neighbor)
        recons_nei = 0
        for i in range(self.args.dataset.num_view):
            recons_nei += l(x_hat[i], neighbor_embedding[i])
        recons_nei /= s[0].shape[0]

        return match_err, recons_err + recons_nei

    # The loss function for independence regularization
    def _loss_independence(self, phi_c_list, psi_p_list):
        def compute_corr(x1, x2):
            # Subtract the mean
            x1_mean = torch.mean(x1, 0, True)
            x1 = x1 - x1_mean
            x2_mean = torch.mean(x2, 0, True)
            x2 = x2 - x2_mean
            # Compute the cross correlation
            sigma1 = torch.sqrt(torch.mean(x1.pow(2)))
            sigma2 = torch.sqrt(torch.mean(x2.pow(2)))
            corr = torch.abs(torch.mean(x1*x2))/(sigma1*sigma2)
            return corr
        
        # Correlation
        corr = 0
        for i in range(len(phi_c_list)):
            corr += compute_corr(phi_c_list[i], psi_p_list[i])
        return corr


    # Contrastive loss
    def _loss_contrastive(self, U, private, adj_list):
        def semi_loss(z1, z2, z3, z4, tau):
            f = lambda x: torch.exp(x / tau)
            positive = f(F.cosine_similarity(z1, z2))
            negative = f(F.cosine_similarity(z3, z4))
            return -torch.log(positive.sum() / (positive.sum() + negative.sum() ))
        i = 0
        loss = 0
        for adj in adj_list:
            adj = adj_list[i]
            out_node = adj.to_sparse()._indices()[1]
            random = np.random.randint(out_node.shape[0], size=int((out_node.shape[0] / self.args.dmg.sample_num)))
            sample_edge = adj.to_sparse()._indices().T[random]
            dis = F.cosine_similarity(U[sample_edge.T[0]],U[sample_edge.T[1]])
            a, maxidx = torch.sort(dis, descending=True)
            idx1 = maxidx[:int(sample_edge.shape[0]*0.2)]
            b, minidx = torch.sort(dis, descending=False)
            idx2 = minidx[:int(sample_edge.shape[0]*0.1)]
            private_sample_0 = private[i][sample_edge[idx1].T[0]]
            private_sample_1 = private[i][sample_edge[idx1].T[1]]
            private_sample_2 = private[i][sample_edge[idx2].T[0]]
            private_sample_3 = private[i][sample_edge[idx2].T[1]]
            i += 1
            loss += semi_loss(private_sample_0, private_sample_1, private_sample_2, private_sample_3, self.args.dmg.tau)
        return loss






# def add_random_edge(edge_index, p: float, force_undirected: bool = False,
#                     num_nodes: Optional[Union[Tuple[int], int]] = None,
#                     training: bool = True):
#     if p < 0. or p > 1.:
#         raise ValueError(f'Ratio of added edges has to be between 0 and 1 '
#                          f'(got {p}')
#     if force_undirected and isinstance(num_nodes, (tuple, list)):
#         raise RuntimeError('`force_undirected` is not supported for'
#                            ' heterogeneous graphs')

#     device = edge_index.device
#     if not training or p == 0.0:
#         edge_index_to_add = torch.tensor([[], []], device=device)
#         return edge_index, edge_index_to_add

#     if not isinstance(num_nodes, (tuple, list)):
#         num_nodes = (num_nodes, num_nodes)
#     num_src_nodes = maybe_num_nodes(edge_index, num_nodes[0])
#     num_dst_nodes = maybe_num_nodes(edge_index, num_nodes[1])

#     num_edges_to_add = round(edge_index.size(1) * p)
#     row = torch.randint(0, num_src_nodes, size=(num_edges_to_add, ))
#     col = torch.randint(0, num_dst_nodes, size=(num_edges_to_add, ))

#     if force_undirected:
#         mask = row < col
#         row, col = row[mask], col[mask]
#         row, col = torch.cat([row, col]), torch.cat([col, row])
#     edge_index_to_add = torch.stack([row, col], dim=0).to(device)
#     edge_index = torch.cat([edge_index, edge_index_to_add], dim=1)
#     return edge_index, edge_index_to_add


# def dropout_edge(edge_index: Tensor, p: float = 0.5,
#                  force_undirected: bool = False,
#                  training: bool = True) -> Tuple[Tensor, Tensor]:

#     if p < 0. or p > 1.:
#         raise ValueError(f'Dropout probability has to be between 0 and 1 '
#                          f'(got {p}')

#     if not training or p == 0.0:
#         edge_mask = edge_index.new_ones(edge_index.size(1), dtype=torch.bool)
#         return edge_index, edge_mask

#     row, col = edge_index

#     edge_mask = torch.rand(row.size(0), device=edge_index.device) >= p

#     if force_undirected:
#         edge_mask[row > col] = False

#     edge_index = edge_index[:, edge_mask]

#     if force_undirected:
#         edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)
#         edge_mask = edge_mask.nonzero().repeat((2, 1)).squeeze()

#     return edge_index, edge_mask





