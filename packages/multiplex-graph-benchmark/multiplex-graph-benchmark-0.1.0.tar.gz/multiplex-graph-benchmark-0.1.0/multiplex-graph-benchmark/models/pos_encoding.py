import os
import pickle

import torch
from torch_geometric.utils import get_laplacian, to_scipy_sparse_matrix, to_dense_adj
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import expm
from scipy.linalg import fractional_matrix_power
# from sklearn.utils.graph_shortest_path import graph_shortest_path
from sklearn.preprocessing import normalize
from sklearn.metrics import pairwise_distances


class PositionEncoding(object):
    def __init__(self, savepath, zero_diag=False):
        self.savepath = savepath
        self.zero_diag = zero_diag

    def apply_to(self, dataset, pe_type, overwrite=False):
        saved_pos_enc = self.load()
        if pe_type == 'abs':
            dataset.abs_pe_list = []
        elif pe_type == 'rel':
            dataset.rel_pe_list = []
        edge_index_list = dataset.edge_index_list
        num_nodes = dataset.nb_nodes
        device = edge_index_list[0].device
        if saved_pos_enc is None or overwrite == True:
            print(f"Preparing {pe_type} PE...")
            pe_list = []
            for i, edge_index in enumerate(edge_index_list):
                pe = self.compute_pe(num_nodes, edge_index)
                pe_list.append(pe)
                if self.zero_diag:
                    pe = pe.clone()
                    pe.diagonal()[:] = 0
                if pe_type == 'abs':
                    dataset.abs_pe_list.append(pe.to(device))
                elif pe_type == 'rel':
                    dataset.rel_pe_list.append(pe.to(device))
            self.save(pe_list)
        else:
            for i, edge_index in enumerate(edge_index_list):
                pe = saved_pos_enc[i]
                if self.zero_diag:
                    pe = pe.clone()
                    pe.diagonal()[:] = 0
                if pe_type == 'abs':
                    dataset.abs_pe_list.append(pe.to(device))
                elif pe_type == 'rel':
                    dataset.rel_pe_list.append(pe.to(device))

        return dataset

    def save(self, pos_enc):
        if not os.path.isfile(self.savepath):
            with open(self.savepath, 'wb') as handle:
                pickle.dump(pos_enc, handle)

    def load(self):
        if not os.path.isfile(self.savepath):
            return None
        with open(self.savepath, 'rb') as handle:
            pos_enc = pickle.load(handle)
        return pos_enc

    def compute_pe(self, num_nodes, edge_index):
        pass


class DiffusionEncoding(PositionEncoding):
    def __init__(self, savepath, beta=1., use_edge_attr=False, normalization=None, zero_diag=False):
        """
        normalization: for Laplacian None. sym or rw
        """
        super().__init__(savepath, zero_diag)
        self.beta = beta
        self.normalization = normalization
        self.use_edge_attr = use_edge_attr

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        edge_attr = edge_attr if self.use_edge_attr else None
        edge_index, edge_attr = get_laplacian(
                edge_index, edge_attr, normalization=self.normalization,
                num_nodes=num_nodes)
        L = to_scipy_sparse_matrix(edge_index, edge_attr).tocsc()
        L = expm(-self.beta * L)
        return torch.from_numpy(L.toarray())


class PStepRWEncoding(PositionEncoding):
    def __init__(self, savepath, p=1, beta=0.5, use_edge_attr=False, normalization=None, zero_diag=False):
        super().__init__(savepath, zero_diag)
        self.p = p
        self.beta = beta
        self.normalization = normalization
        self.use_edge_attr = use_edge_attr

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        edge_attr = edge_attr if self.use_edge_attr else None
        edge_index, edge_attr = get_laplacian(
            edge_index, edge_attr, normalization=self.normalization,
            num_nodes=num_nodes)
        L = to_scipy_sparse_matrix(edge_index, edge_attr).tocsc()
        L = sp.identity(L.shape[0], dtype=L.dtype) - self.beta * L
        tmp = L
        for _ in range(self.p - 1):
            tmp = tmp.dot(L)
        return torch.from_numpy(tmp.toarray())


class AdjEncoding(PositionEncoding):
    def __init__(self, savepath, normalization=None, zero_diag=False):
        super().__init__(savepath, zero_diag)
        self.normalization = normalization

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        return to_dense_adj(edge_index)


class FullEncoding(PositionEncoding):
    def __init__(self, savepath, zero_diag=False):
        super().__init__(savepath, zero_diag)

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        return torch.ones((num_nodes, num_nodes))


## Absolute position encoding
class LapEncoding(PositionEncoding):
    def __init__(self, savepath, dim, use_edge_attr=False, normalization=None, zero_diag=False):
        super().__init__(savepath, zero_diag)
        self.pos_enc_dim = dim
        self.normalization = normalization
        self.use_edge_attr = use_edge_attr

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        edge_attr = edge_attr if self.use_edge_attr else None
        edge_index, edge_attr = get_laplacian(
            edge_index, edge_attr, normalization=self.normalization,
            num_nodes=num_nodes)
        L = to_scipy_sparse_matrix(edge_index, edge_attr, num_nodes).tocsc()
        EigVal, EigVec = np.linalg.eig(L.toarray())
        idx = EigVal.argsort() # increasing order
        EigVal, EigVec = EigVal[idx], np.real(EigVec[:,idx])
        return torch.from_numpy(EigVec[:, 1:self.pos_enc_dim+1]).float()


POSENCODINGS = {
    "diffusion": DiffusionEncoding,
    "pstep": PStepRWEncoding,
    "adj": AdjEncoding,
}




class WLKernelEncoding(PositionEncoding):
    def __init__(self, savepath, num_iterations=2, use_edge_attr=False, normalization=None, zero_diag=False):
        super().__init__(savepath, zero_diag)
        self.num_iterations = num_iterations
        self.use_edge_attr = use_edge_attr
        self.normalization = normalization

    def compute_pe(self, num_nodes, edge_index, edge_attr=None):
        edge_attr = edge_attr if self.use_edge_attr else None
        edge_index, edge_attr = get_laplacian(
            edge_index, edge_attr, normalization=self.normalization,
            num_nodes=num_nodes)
        adjacency_matrix = to_scipy_sparse_matrix(edge_index, edge_attr).tocsc()

        # Initial node labels (unique node degrees)
        node_labels = np.asarray(adjacency_matrix.sum(axis=0)).squeeze()

        # Iterate WL kernel updates
        for iteration in range(self.num_iterations):
            # Apply WL kernel update
            adjacency_matrix = self.wl_kernel_update(adjacency_matrix, node_labels)

            # Update node labels
            node_labels = self.compute_node_labels(adjacency_matrix)

        # Normalize the resulting adjacency matrix
        adjacency_matrix = normalize(adjacency_matrix, norm='l1', axis=1)

        return torch.from_numpy(adjacency_matrix.toarray())

    def wl_kernel_update(self, adjacency_matrix, node_labels):
        """
        Update the adjacency matrix using the Weisfeiler-Leman kernel update.
        """
        num_nodes = adjacency_matrix.shape[0]

        # Create a copy of the adjacency matrix
        updated_adjacency_matrix = adjacency_matrix.copy()

        # Iterate over each node
        for i in range(num_nodes):
            # Get the neighbors of the current node
            neighbors = np.nonzero(adjacency_matrix[i])[0]

            # Concatenate the node label and the labels of its neighbors
            labels = np.concatenate([[node_labels[i]], node_labels[neighbors]])

            # Use the concatenated labels to create a unique label
            unique_label = hash(tuple(labels))

            # Update the adjacency matrix with the unique label
            updated_adjacency_matrix[i, :] = 0
            updated_adjacency_matrix[:, i] = 0
            updated_adjacency_matrix[i, i] = unique_label

        return updated_adjacency_matrix

    def compute_node_labels(self, adjacency_matrix):
        """
        Compute node labels from the updated adjacency matrix.
        """
        num_nodes = adjacency_matrix.shape[0]
        node_labels = np.zeros(num_nodes, dtype=int)

        # Assign labels based on the unique entries in the adjacency matrix
        unique_labels = np.unique(adjacency_matrix)
        label_mapping = {label: i for i, label in enumerate(unique_labels)}

        # Update node labels
        for i in range(num_nodes):
            node_labels[i] = label_mapping[adjacency_matrix[i, i]]

        return node_labels