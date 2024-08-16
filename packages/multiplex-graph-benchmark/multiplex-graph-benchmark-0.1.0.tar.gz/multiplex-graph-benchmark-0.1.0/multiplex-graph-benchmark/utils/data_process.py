import torch
import numpy as np
import pickle as pkl
import scipy.io as sio
import scipy.sparse as sp
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import random as random
import os
import os.path as osp
from collections.abc import Sequence
from typing import Any, Callable, List, Optional, Tuple, Union
import errno


class Dataset(torch.utils.data.Dataset):
    def __init__(self, cfg):
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self._download()
        self._process()

        dataset = torch.load(self.processed_paths[0], map_location=self.device)
        self.features = dataset['features'].to(self.device)
        self.labels = dataset['labels'].to(self.device)
        self.adj_list =  dataset['adj_list']                #[adj.to(self.device) for adj in dataset['adj_list']]
        self.edge_index_list =  dataset['edge_index_list']  #[edge_index.to(self.device) for edge_index in dataset['edge_index_list']]
        self.idx_train = dataset['idx_train']
        self.idx_val = dataset['idx_val']
        self.idx_test = dataset['idx_test']
        self.edge_labels = dataset['edge_labels']
        self.edge_idx_train = dataset['edge_idx_train']
        self.edge_idx_test = dataset['edge_idx_test']

        self.ft_size = self.features.shape[1]
        self.nb_classes = self.labels.shape[1]
        self.nb_nodes = self.adj_list[0].shape[1]
        self.nb_edges = [edge_index.shape[1] for edge_index in self.edge_index_list]
        self.num_view = len(self.adj_list)

        # update dataset cfgs
        cfg.dataset.nb_nodes = self.nb_nodes
        cfg.dataset.nb_classes = self.nb_classes
        cfg.dataset.ft_size = self.ft_size
        cfg.dataset.num_view = self.num_view

    @property
    def raw_dir(self):
        return os.path.join(self.args.dataset.root, self.args.dataset_name, 'raw')


    @property
    def processed_dir(self):
        return os.path.join(self.args.dataset.root, self.args.dataset_name, 'processed')

 
    @property
    def raw_file_names(self):
        if self.args.dataset_name.lower() == 'acm':
            return ['ACM3025.mat']  
        elif self.args.dataset_name.lower() == 'acm2':
            return ['acm2_vec.mat']
        elif self.args.dataset_name.lower() == 'imdb':
            return ['IMDB4780.mat'] 
        elif self.args.dataset_name.lower() == 'imdb2':
            return ['imdb2_vec.mat'] 
        elif self.args.dataset_name.lower() == 'dblp':
            return ['DBLP4057.mat'] 
        elif self.args.dataset_name.lower() == 'dblp2':
            return ['dblp2_vec.mat'] 
        elif self.args.dataset_name.lower() == 'amazon':
            return ['AMAZON7621.pkl'] 
        elif self.args.dataset_name.lower() == 'amazon2':
            return ['amazon2_vec.mat']  
        elif self.args.dataset_name.lower() == 'freebase':
            return ['labels.npy','mam.npz','mdm.npz','mwm.npz']
        elif self.args.dataset_name.lower() == 'amazon_fraud':
            return ['Amazon_fraud.mat']
        elif self.args.dataset_name.lower() == 'yelpchi_fraud':
            return ['YelpChi_fraud.mat']


    @property
    def processed_file_names(self):
        if self.args.dataset_name.lower() == 'acm':
            return ['acm_processed.pt']  
        elif self.args.dataset_name.lower() == 'acm2':
            return ['acm2_processed.pt']
        elif self.args.dataset_name.lower() == 'imdb':
            return ['imdb_processed.pt'] 
        elif self.args.dataset_name.lower() == 'imdb2':
            return ['imdb2_processed.pt'] 
        elif self.args.dataset_name.lower() == 'dblp':
            return ['dblp_processed.pt'] 
        elif self.args.dataset_name.lower() == 'dblp2':
            return ['dblp2_processed.pt'] 
        elif self.args.dataset_name.lower() == 'amazon':
            return ['amazon_processed.pt'] 
        elif self.args.dataset_name.lower() == 'amazon2':
            return ['amazon2_processed.pt']  
        elif self.args.dataset_name.lower() == 'freebase':
            return ['freebase_processed.pt']
        elif self.args.dataset_name.lower() == 'amazon_fraud':
            return ['amazon_fraud_processed.pt']
        elif self.args.dataset_name.lower() == 'yelpchi_fraud':
            return ['yelpchi_fraud_processed.pt']

    @property
    def meta_path_names(self):
        if self.args.dataset_name.lower() == "acm":
            return ["PLP","PAP"]
        elif self.args.dataset_name.lower() == "acm2":
            return ["PLP","PAP"]
        elif self.args.dataset_name.lower() == "imdb":
            return ["MAM","MDM"]
        elif self.args.dataset_name.lower() == "imdb2":
            return ["MAM","MDM"]
        elif self.args.dataset_name.lower() == "dblp":
            return ["net_APTPA","net_APCPA","net_APA"]
        elif self.args.dataset_name.lower() == "dblp2":
            return ["PAP","PPP","PATAP"]
        elif self.args.dataset_name.lower() == "amazon":
            return ["IVI","IBI","IOI"]
        elif self.args.dataset_name.lower() == "amazon2":
            return ["IVI","IBI","IOI"]
        elif self.args.dataset_name.lower() == "amazon_fraud":
            return ["net_upu","net_usu","net_uvu"]
        elif self.args.dataset_name.lower() == "yelpchi_fraud":
            return ["net_rur","net_rtr","net_rsr"]

    @property
    def raw_paths(self):
        files = self.raw_file_names
        if isinstance(files, Callable):
            files = files()
        return [osp.join(self.raw_dir, f) for f in to_list(files)]
    

    @property
    def processed_paths(self):
        files = self.processed_file_names
        if isinstance(files, Callable):
            files = files()
        return [osp.join(self.processed_dir, f) for f in to_list(files)]


    def _download(self):
        if files_exist(self.raw_paths):
            return
        # makedirs(self.raw_dir)
        # download code


    def _process(self):            
        if files_exist(self.processed_paths):
            return
        makedirs(self.processed_dir)

        ### load raw data
        if self.args.dataset_name.lower() == "freebase":
            adj_list, features, labels, idx_train, idx_val, idx_test = self.load_freebase(self.raw_dir, self.args.dataset.sc)
        else:
            meta_paths = self.meta_path_names
            adj_list, features, labels, idx_train, idx_val, idx_test = self.load_data(self.raw_paths, meta_paths, self.args.dataset.sc)
            features = preprocess_features(features)
        features = torch.FloatTensor(features)
        labels = torch.FloatTensor(labels)
        num_nodes = features.shape[0]


        ### transform and normalize adjacency matrix
        adj_list = [sparse_mx_to_torch_sparse_tensor(adj) for adj in adj_list]
        adj_list = [adj.to_dense() for adj in adj_list]
        adj_list = [normalize_graph(adj) for adj in adj_list]
        # if self.args.dataset.sparse:
        #     adj_list = [adj.to_sparse() for adj in adj_list]


        ### Edge Classification & Prediction
        edge_labels = dict()
        edge_idx_train = dict()
        edge_idx_test = dict()

        ### EC
        edge_index_list = []
        edge_labels_list = []
        for i, adj in enumerate(adj_list):
            edge_index = torch.nonzero(adj, as_tuple=False).t().long()
            e_labels = torch.zeros(edge_index.size(1), len(adj_list))  # Initialize with zeros
            e_labels[:, i] = 1
            edge_index_list.append(edge_index)
            edge_labels_list.append(e_labels)
        edge_labels['classification'] = torch.cat(edge_labels_list, dim=0)
        num_edges = edge_labels['classification'].shape[0]

        budget = 10000
        e_idx_train = []
        e_idx_test = []
        for class_idx in range(edge_labels['classification'].size(1)):
            class_indices = np.where(edge_labels['classification'][:, class_idx] == 1)[0]
            np.random.shuffle(class_indices)
            sample_num = min(budget, len(class_indices))
            sampled_indices = class_indices[:sample_num]
            num_samples_train = int(0.8*len(sampled_indices))
            num_samples_test = len(sampled_indices) - num_samples_train
            e_idx_train.extend(sampled_indices[:num_samples_train])
            e_idx_test.extend(sampled_indices[num_samples_train:])
        edge_idx_train['classification'] = torch.from_numpy(np.array(e_idx_train)).long()
        edge_idx_test['classification'] = torch.from_numpy(np.array(e_idx_test)).long()


        ### EP
        edge_index_all = torch.cat(edge_index_list, dim=1)
        u, v = edge_index_all
        eids = np.arange(num_edges)
        eids = np.random.permutation(eids)
        budget = 10000
        sample_num = min(budget, len(eids))
        test_size = int(sample_num * 0.2)
        train_size = sample_num - test_size
        test_pos_u, test_pos_v = u[eids[:test_size]], v[eids[:test_size]]
        train_pos_u, train_pos_v = u[eids[test_size:test_size+train_size]], v[eids[test_size:test_size+train_size]]

        neg_ratio = 5
        neg_sample_num = min(neg_ratio * budget, len(eids))
        neg_test_size = int(neg_sample_num * 0.2)
        neg_train_size = neg_sample_num - neg_test_size
        adj = sp.coo_matrix((np.ones(len(u)), (u.numpy(), v.numpy())))
        adj_neg = 1 - adj.todense() - np.eye(num_nodes)
        neg_u, neg_v = np.where(adj_neg != 0)
        neg_eids = np.random.choice(len(neg_u), neg_sample_num)
        test_neg_u, test_neg_v = (neg_u[neg_eids[:neg_test_size]], neg_v[neg_eids[:neg_test_size]])
        train_neg_u, train_neg_v = (neg_u[neg_eids[neg_test_size:neg_test_size+neg_train_size]], neg_v[neg_eids[neg_test_size:neg_test_size+neg_train_size]])

        train_u = torch.cat([train_pos_u, torch.from_numpy(train_neg_u).long()])
        train_v = torch.cat([train_pos_v, torch.from_numpy(train_neg_v).long()])
        test_u = torch.cat([test_pos_u, torch.from_numpy(test_neg_u).long()])
        test_v = torch.cat([test_pos_v, torch.from_numpy(test_neg_v).long()])
        edge_idx_train['prediction'] = torch.stack([train_u, train_v], dim=0)
        edge_idx_test['prediction'] = torch.stack([test_u, test_v], dim=0)

        train_labels = torch.cat([torch.ones(len(train_pos_u)), torch.zeros(len(train_neg_u))])
        test_labels = torch.cat([torch.ones(len(test_pos_u)), torch.zeros(len(test_neg_u))])
        edge_labels['prediction'] = torch.cat([train_labels, test_labels]).view(-1,1)


        ### Save to .pt
        dataset = {
            'features': features,               #[num_nodes, dim]
            'labels': labels,                   #[num_nodes, num_classes]
            'edge_labels': edge_labels,         #cls:[num_edges, num_classes_edge]; pre[num_edges, 1]
            'adj_list': adj_list,               #[num_nodes, num_nodes]
            'edge_index_list': edge_index_list, #[num_views, 2, num_edges_each_view]
            'idx_train': idx_train,
            'idx_val': idx_val,
            'idx_test': idx_test,
            'edge_idx_train': edge_idx_train,
            'edge_idx_test': edge_idx_test
        }
        torch.save(dataset, self.processed_paths[0])


    def __len__(self):
        return self.nb_nodes
    
    def __getitem__(self, idx):
        return self.tf_input_list[:,idx,:,:], self.pos_attention_list[:,idx,:,:], self.padding_list[:,idx,:], self.labels[idx]


    def load_data(self, root, meta_paths, sc=3):
        ### load data file
        if 'AMAZON7621' in root[0]:
            data = pkl.load(open(root[0], "rb"))
        else:
            data = sio.loadmat(root[0])

        ### labels
        label = data['label']

        ### adj_list
        adj_list = []
        for meta_path in meta_paths:
            adj = data[meta_path] + np.eye(data[meta_path].shape[0])*sc
            adj = sp.csr_matrix(adj)
            adj_list.append(adj)

        ### features
        if any(sub in root[0] for sub in ['DBLP4057', 'Amazon_fraud', 'YelpChi_fraud']):
            truefeatures = data['features'].astype(float)
        else:
            truefeatures = data['feature'].astype(float)
        truefeatures = sp.lil_matrix(truefeatures)

        ### train/val/test idx
        if "Amazon_fraud" in root[0] or "YelpChi_fraud" in root[0]:
            num_classes = 2
            idx_train = np.array([], dtype=int)
            idx_val = np.array([], dtype=int)
            idx_test = np.array([], dtype=int)
            train_ratio = 0.2
            val_ratio = 0.1
            test_ratio = 0.7
            for class_label in range(num_classes):
                class_indices = np.where(label == class_label)[0]
                np.random.shuffle(class_indices)
                num_nodes = len(class_indices)
                num_train = int(train_ratio * num_nodes)
                num_val = int(val_ratio * num_nodes)
                idx_train = np.concatenate((idx_train, class_indices[:num_train]))
                idx_val = np.concatenate((idx_val, class_indices[num_train:num_train + num_val]))
                idx_test = np.concatenate((idx_test, class_indices[num_train + num_val:]))
            np.random.shuffle(idx_train)
            np.random.shuffle(idx_val)
            np.random.shuffle(idx_test) 
            label = label.flatten().astype(int) 
            one_hot_labels = np.eye(num_classes)[label]    
            label = one_hot_labels  
        else:
            idx_train = data['train_idx'].ravel()
            idx_val = data['val_idx'].ravel()
            idx_test = data['test_idx'].ravel()
        
        return adj_list, truefeatures, label, idx_train, idx_val, idx_test


    def load_freebase(self, root, sc=3):
        type_num = 3492
        ratio = [20, 40, 60]
        # The order of node types: 0 m 1 d 2 a 3 w
        path = root + "/"
        label = np.load(path + "labels.npy").astype('int32')
        label = encode_onehot(label)
        feat_m = sp.eye(type_num)
        # Because none of M, D, A or W has features, we assign one-hot encodings to all of them.
        mam = sp.load_npz(path + "mam.npz")
        mdm = sp.load_npz(path + "mdm.npz")
        mwm = sp.load_npz(path + "mwm.npz")
        train = [np.load(path + "train_" + str(i) + ".npy") for i in ratio]
        test = [np.load(path + "test_" + str(i) + ".npy") for i in ratio]
        val = [np.load(path + "val_" + str(i) + ".npy") for i in ratio]

        label = torch.FloatTensor(label)
        feat_m = torch.FloatTensor(preprocess_features(feat_m))
        adj_list = [mam, mdm, mwm]
        train = [torch.LongTensor(i) for i in train]
        val = [torch.LongTensor(i) for i in val]
        test = [torch.LongTensor(i) for i in test]
        return  adj_list, feat_m, label, train[0], val[0], test[0]


    # MG-tf modification
    def update_features(self, path, overwrite):
        if not os.path.isfile(path) or overwrite == True:
            print("Preparing tf_input_list...")
            assert self.abs_pe_list is not None
            assert self.rel_pe_list is not None
            tf_input_list, pos_attention_list, padding_list = self._create_padded_sequences(self.adj_list, self.abs_pe_list, self.rel_pe_list, self.features, self.args.mgtf.seq_len)
            torch.save({'tf_input_list':tf_input_list, 'pos_attention_list':pos_attention_list, 'padding_list':padding_list}, path)
        file = torch.load(path, map_location=self.device)
        self.tf_input_list = file['tf_input_list'].to(self.device)
        self.pos_attention_list = file['pos_attention_list'].to(self.device)
        self.padding_list = file['padding_list'].to(self.device)


    # MG-tf modification
    def _create_padded_sequences(self, adj_list, abs_pe_list, rel_pe_list, features, L):
        pad_value = 0
        gathered_features_list = []
        pos_attention_list = []
        padding_mask_list = []

        for adj, abs_pe, rel_pe in zip(adj_list, abs_pe_list, rel_pe_list):
            adj.diagonal()[:] = 0   # remove the node itself
            # Dynamic Sequence
            # avg_degree = int((adj.sum() // adj.size(0)).item())
            # L = avg_degree if avg_degree < 256 else 256
            gathered_features_graph = []
            pos_attention_graph = []
            padding_mask_graph = []
            for node_idx, diffusion_values in enumerate(adj):
                non_zero_indices = torch.nonzero(diffusion_values).squeeze(1)
                sorted_indices = non_zero_indices[torch.argsort(diffusion_values[non_zero_indices], descending=True)].tolist()
                sampled_neighbors = [node_idx] + sorted_indices[:min(L-1, len(sorted_indices))]

                gathered_features = torch.full((L, features.size(1)+abs_pe.size(1)), pad_value, dtype=features.dtype)
                # gathered_features = torch.full((L, features.size(1)), pad_value, dtype=features.dtype)
                pos_attention = torch.zeros((L, L), dtype=features.dtype)
                padding_mask = torch.zeros(L, dtype=torch.bool)

                gathered_features[:len(sampled_neighbors)] = torch.cat((features[sampled_neighbors], abs_pe[sampled_neighbors]), dim=-1)
                # gathered_features[:len(sampled_neighbors)] = features[sampled_neighbors]
                pos_attention[:len(sampled_neighbors), :len(sampled_neighbors)] = rel_pe[sampled_neighbors][:,sampled_neighbors]
                padding_mask[:len(sampled_neighbors)] = 1

                gathered_features_graph.append(gathered_features)
                pos_attention_graph.append(pos_attention)
                padding_mask_graph.append(padding_mask)

            gathered_features_list.append(torch.stack(gathered_features_graph, dim=0))
            pos_attention_list.append(torch.stack(pos_attention_graph, dim=0))
            padding_mask_list.append(torch.stack(padding_mask_graph, dim=0))

        return torch.stack(gathered_features_list, dim=0), torch.stack(pos_attention_list, dim=0), torch.stack(padding_mask_list, dim=0)


def encode_onehot(labels):
    labels = labels.reshape(-1, 1)
    enc = OneHotEncoder()
    enc.fit(labels)
    labels_onehot = enc.transform(labels).toarray()
    return labels_onehot


def preprocess_features(features):
    """Row-normalize feature matrix and convert to tuple representation"""
    rowsum = np.array(features.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    features = r_mat_inv.dot(features)
    return features.todense()


def normalize_graph(A):
    eps = 2.2204e-16
    deg_inv_sqrt = (A.sum(dim=-1).clamp(min=0.) + eps).pow(-0.5)
    if A.size()[0] != A.size()[1]:
        A = deg_inv_sqrt.unsqueeze(-1) * (deg_inv_sqrt.unsqueeze(-1) * A)
    else:
        A = deg_inv_sqrt.unsqueeze(-1) * A * deg_inv_sqrt.unsqueeze(-2)
    return A


def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)


def makedirs(path: str):
    r"""Recursively creates a directory.

    Args:
        path (str): The path to create.
    """
    try:
        os.makedirs(osp.expanduser(osp.normpath(path)))
    except OSError as e:
        if e.errno != errno.EEXIST and osp.isdir(path):
            raise e


def to_list(value: Any) -> Sequence:
    if isinstance(value, Sequence) and not isinstance(value, str):
        return value
    else:
        return [value]


def files_exist(files: List[str]) -> bool:
    # NOTE: We return `False` in case `files` is empty, leading to a
    # re-processing of files on every instantiation.
    return len(files) != 0 and all([osp.exists(f) for f in files])