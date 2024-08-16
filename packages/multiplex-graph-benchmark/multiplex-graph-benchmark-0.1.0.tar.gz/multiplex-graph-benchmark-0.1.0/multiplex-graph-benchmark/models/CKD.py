import torch
import torch.nn as nn
import numpy as np
import random as random
from sklearn.utils import shuffle

from models.CKD_utils import PPR, get_topk_neigh_multi, Encoder


class CKD(nn.Module):
    def __init__(self, cfg):
        super(CKD, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")
        self.criteria = nn.BCEWithLogitsLoss()
        self.enc = Encoder(cfg.dataset.ft_size, cfg.gnn.hidden_dim, cfg.gnn.layers)
        self.init_weight()

    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0) 

    def forward(self, data, optimizer, epoch):
        total_loss = 0.0
        train_views = shuffle(data.sample_train_views)
        total_train_views = data.total_train_views
        steps = (len(train_views) // self.args.ckd.batch_size) + (0 if len(train_views) % self.args.ckd.batch_size == 0 else 1)

        # get global emb
        global_graph_emb_list = []
        neg_global_graph_emb_list = []
        for channel in range(self.args.dataset.num_view):
            train_features = torch.cat([i[2][channel][2] for i in total_train_views], dim=0)
            neg_features = torch.cat([i[2][channel][3] for i in total_train_views], dim=0)
            train_adj = torch.cat([i[2][channel][1] for i in total_train_views], dim=0)

            emb, graph_emb = self.enc(train_features, train_adj)
            neg_emb, neg_graph_emb = self.enc(neg_features, train_adj)

            index = torch.Tensor([0]).long().cuda()
            emb = emb.index_select(dim=1, index=index).squeeze()
            global_emb = torch.mean(emb, dim=0).detach()
            neg_emb = neg_emb.index_select(dim=1, index=index).squeeze()
            global_neg_emb = torch.mean(neg_emb, dim=0).detach()

            global_graph_emb_list.append(global_emb)
            neg_global_graph_emb_list.append(global_neg_emb)

        for step in range(steps):
            optimizer.zero_grad()
            start = step * self.args.ckd.batch_size
            end = min((step + 1) * self.args.ckd.batch_size, len(train_views))
            if end-start <= 1:
                continue
            step_train_views = train_views[start:end]

            emb_list = []
            graph_emb_list = []
            for channel in range(self.args.dataset.num_view):
                train_features = torch.cat([i[2][channel][2] for i in step_train_views], dim=0)
                train_adj = torch.cat([i[2][channel][1] for i in step_train_views], dim=0)
                emb, graph_emb = self.enc(train_features, train_adj)
                emb_list.append(emb)
                graph_emb_list.append(graph_emb)

            local_loss = self._score(self.criteria, emb_list, graph_emb_list,[i[1] for i in step_train_views])
            global_loss = self._global_score(self.criteria, emb_list, global_graph_emb_list, neg_global_graph_emb_list, [i[1] for i in step_train_views])
            loss = local_loss + global_loss * self.args.ckd.global_weight
            total_loss += loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.parameters(), 5.0)
            optimizer.step()

        return total_loss
       
    
    def get_embedding(self, data):
        emb_list = []
        for channel in range(self.args.dataset.num_view):
            train_features = torch.cat([i[2][channel][2] for i in data.total_train_views], dim=0)
            train_adj = torch.cat([i[2][channel][1] for i in data.total_train_views], dim=0)
            emb, graph_emb = self.enc(train_features, train_adj)
            index = torch.Tensor([0]).long().cuda()
            emb = emb.index_select(dim=1, index=index).squeeze()
            emb_list.append(emb)
        emb_list = torch.stack(emb_list, dim=0)
        return torch.mean(emb_list, dim=0).detach()  

    def preprocess(self, data):
        features = data.features
        shuffle_embeddings = torch.from_numpy(shuffle(np.array(features.cpu()))).to(self.device)
        adj_list = [np.array(adj_.cpu()) for adj_ in data.adj_list]

        target_nodes = np.array(list(range(self.args.dataset.nb_nodes)))
        node2neigh_list = []
        for view in range(self.args.dataset.num_view):
            node2neigh = []
            adj = adj_list[view]
            for node in range(self.args.dataset.nb_nodes):
                neighbors = np.nonzero(adj[node])[0].tolist()
                node2neigh.append(neighbors)
            node2neigh_list.append(node2neigh)
        
        # SubGraph Sampling
        sim_matrix_list = PPR(adj_list)
        total_train_views = get_topk_neigh_multi(target_nodes, node2neigh_list, self.args.ckd.topk, adj_list, sim_matrix_list)

        for node,status,view in total_train_views:
            for channel_data in view:
                channel_data[0] = torch.from_numpy(channel_data[0]).to(self.device)
                channel_data[1] = torch.from_numpy(channel_data[1]).float().to(self.device)
                datass = features[channel_data[0]]
                channel_data.append(datass.reshape(1,datass.shape[0],datass.shape[1]))
                shuffle_data = shuffle_embeddings[channel_data[0]]
                channel_data.append(shuffle_data.reshape(1, shuffle_data.shape[0], shuffle_data.shape[1]))

        sample_train_views = [i for i in total_train_views if sum(i[1])>=1]
        print(f'context subgraph num:{len(sample_train_views)}')    

        ### CKD converts necessary data into total_train_views & sample_train_views
        data.total_train_views = total_train_views
        data.sample_train_views = sample_train_views
        # data.features = data.features.to(self.device)
        # data.adj_list = [adj.to(self.device) for adj in data.adj_list]

    def postprocess(self, data):
        pass


    def _score(self, criterion, emb_list, graph_emb_list, status_list):
        index = torch.Tensor([0]).long().cuda()
        loss = None
        for idx in range(len(emb_list)):
            emb_list[idx]=emb_list[idx].index_select(dim=1, index=index).squeeze()
        for idx in range(len(emb_list)):
            for idy in range(len(emb_list)):
                node_emb = emb_list[idx]
                graph_emb=graph_emb_list[idy]
                mask = torch.Tensor([i[idy] for i in status_list]).bool().cuda()
                pos = torch.sum(node_emb * graph_emb, dim=1).squeeze().masked_select(mask)
                matrix = torch.mm(node_emb, graph_emb.T)
                mask_idx = torch.Tensor([i for i in range(len(status_list)) if status_list[i][idy] == 0]).long().cuda()
                neg_mask = np.ones(shape=(node_emb.shape[0], node_emb.shape[0]))
                row, col = np.diag_indices_from(neg_mask)
                neg_mask[row, col] = 0
                neg_mask = torch.from_numpy(neg_mask).bool().cuda()
                neg_mask[mask_idx,] = 0
                neg = matrix.masked_select(neg_mask)

                if pos.shape[0]==0:
                    continue
                if loss is None:
                    loss = criterion(pos, torch.from_numpy(np.array([1] * pos.shape[0])).float().cuda())
                    loss += criterion(neg, torch.from_numpy(np.array([0] * neg.shape[0])).float().cuda())
                else:
                    loss += criterion(pos, torch.from_numpy(np.array([1] * pos.shape[0])).float().cuda())
                    loss += criterion(neg, torch.from_numpy(np.array([0] * neg.shape[0])).float().cuda())
        return loss


    def _global_score(self, criterion, emb_list, graph_emb_list, neg_graph_emb_list, status_list):
        loss = None
        for idx in range(len(emb_list)):
            for idy in range(len(emb_list)):
                node_emb=emb_list[idx]
                global_emb=graph_emb_list[idy]
                neg_global_emb=neg_graph_emb_list[idy]
                mask = torch.Tensor([i[idx] for i in status_list]).bool().cuda()
                pos = torch.sum(node_emb * global_emb, dim=1).squeeze().masked_select(mask)
                neg = torch.sum(node_emb * neg_global_emb, dim=1).squeeze().masked_select(mask)
                if pos.shape[0]==0:
                    continue

                if loss is None:
                    loss = criterion(pos, torch.from_numpy(np.array([1] * pos.shape[0])).float().cuda())
                    loss += criterion(neg, torch.from_numpy(np.array([0] * neg.shape[0])).float().cuda())
                else:
                    loss += criterion(pos, torch.from_numpy(np.array([1] * pos.shape[0])).float().cuda())
                    loss += criterion(neg, torch.from_numpy(np.array([0] * neg.shape[0])).float().cuda())
        return loss