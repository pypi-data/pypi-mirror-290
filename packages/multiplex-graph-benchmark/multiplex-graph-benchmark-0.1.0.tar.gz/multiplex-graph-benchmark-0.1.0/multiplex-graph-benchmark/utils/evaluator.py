import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random as random
from sklearn.cluster import KMeans
from sklearn import metrics
from munkres import Munkres




class LogReg(nn.Module):
    def __init__(self, ft_in, nb_classes, dropout=0.1):
        super(LogReg, self).__init__()
        self.fc = nn.Linear(ft_in, nb_classes)
        self.dropout = nn.Dropout(p=dropout)

        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    def forward(self, seq):
        seq = self.dropout(seq)
        seq = self.fc(seq)
        seq = F.softmax(seq, dim=1)
        return seq


class BinaryCls(nn.Module):
    def __init__(self, ft_in, nb_classes, dropout=0.1):
        super(BinaryCls, self).__init__()

        self.fc1 = nn.Linear(ft_in, 64)
        self.fc2 = nn.Linear(64, 8)
        self.fc3 = nn.Linear(8, nb_classes)  # Output dimension is 1 for binary classification
        self.dropout = nn.Dropout(p=dropout)

        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    def forward(self, seq):
        seq = self.dropout(seq)
        seq = F.relu(self.fc1(seq)) 
        seq = self.dropout(seq)
        seq = F.relu(self.fc2(seq)) 
        seq = self.dropout(seq)
        seq = self.fc3(seq)  
        seq = torch.sigmoid(seq)  
        return seq


class Evaluator():
    def __init__(self, epochs, lr, iterater=10):
        self.epoch = epochs
        self.lr = lr
        self.iterater = iterater
        self.xent = nn.CrossEntropyLoss()
        self.bce = nn.BCEWithLogitsLoss()


    def edge_prediction(self, embedding, edge_index_train, edge_index_test, edge_labels):
        train_embs = torch.cat([embedding[edge_index_train[0]], embedding[edge_index_train[1]]], dim=1).to(embedding.device)
        test_embs = torch.cat([embedding[edge_index_test[0]], embedding[edge_index_test[1]]], dim=1).to(embedding.device)
        train_size = edge_index_train.shape[1]
        train_lbls = edge_labels[:train_size].view(-1, 1).to(embedding.device)
        test_lbls = edge_labels[train_size:].view(-1, 1)

        log = BinaryCls(embedding.shape[1]*2, 1).to(embedding.device)
        opt = torch.optim.Adam(log.parameters(), lr=0.1)

        log.train()
        for iter_ in range(self.epoch):
            opt.zero_grad()
            output = log(train_embs)
            train_loss = self.bce(output, train_lbls)
            train_loss.backward()
            opt.step()

        log.eval()
        with torch.no_grad():
            test_output = log(test_embs)
            test_preds = (test_output > 0.5).int().view(-1, 1)

        #AUC_ROC
        auc_roc = metrics.roc_auc_score(test_lbls.cpu().numpy(), test_output.cpu().numpy())
        precision, recall, _ = metrics.precision_recall_curve(test_lbls.cpu().numpy(), test_output.cpu().numpy())
        auc_pr = metrics.auc(recall, precision)
        f1 = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='weighted')
        def mean_reciprocal_rank(labels, scores):
            order = np.argsort(-scores)  # Sort in descending order
            ranks = np.where(labels[order] == 1)[0] + 1  # Get ranks (1-based)
            return np.mean(1.0 / ranks) if len(ranks) > 0 else 0.0
        mrr = mean_reciprocal_rank(test_lbls.cpu().numpy(), test_output.cpu().numpy())

        return auc_roc, auc_pr, f1, mrr


    def edge_classification(self, embedding, edge_index_list, edge_labels, idx_train, idx_test):
        edge_index = torch.cat(edge_index_list, dim=1)
        edge_index_train = edge_index[:,idx_train]
        edge_index_test = edge_index[:,idx_test]
        train_embs = torch.cat([embedding[edge_index_train[0]], embedding[edge_index_train[1]]], dim=1).to(embedding.device)
        test_embs = torch.cat([embedding[edge_index_test[0]], embedding[edge_index_test[1]]], dim=1).to(embedding.device)
        train_lbls = torch.argmax(edge_labels[idx_train],dim=1).to(embedding.device)
        test_lbls = torch.argmax(edge_labels[idx_test],dim=1)

        log = LogReg(embedding.shape[1]*2, edge_labels.shape[1]).to(embedding.device)
        opt = torch.optim.Adam(log.parameters(), lr=self.lr)

        log.train()
        for iter_ in range(self.epoch):
            opt.zero_grad()
            output = log(train_embs)
            train_loss = self.xent(output, train_lbls)
            train_loss.backward()
            opt.step()

        log.eval()
        with torch.no_grad():
            test_output = log(test_embs)
            test_preds = torch.argmax(test_output, dim=1)

        #AUC-ROC and AUC-PR
        auc_roc_list = []
        auc_pr_list = []
        for i in range(test_output.shape[1]):
            auc_roc_i = metrics.roc_auc_score(edge_labels[idx_test, i].cpu().numpy(), test_output[:, i].cpu().numpy())
            auc_pr_i = metrics.average_precision_score(edge_labels[idx_test, i].cpu().numpy(), test_output[:, i].cpu().numpy())
            auc_roc_list.append(auc_roc_i)
            auc_pr_list.append(auc_pr_i)
        auc_roc = sum(auc_roc_list) / len(auc_roc_list)
        auc_pr = sum(auc_pr_list) / len(auc_pr_list)
        #acc
        accuracy = metrics.accuracy_score(test_lbls.cpu(), test_preds.cpu())
        #F1
        f1 = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='weighted')
        return accuracy, f1
        

    def node_classification_multi_label(self, flag, embedding, idx_train, idx_test, labels):
        test_lbls = labels[idx_test]  # Get test labels
        if flag == "ss":
            train_embs = embedding[idx_train]
            test_embs = embedding[idx_test]
            nb_classes = labels.shape[1]
            train_labels = labels[idx_train]
            log = LogReg(train_embs.shape[1], nb_classes).to(labels.device)
            opt = torch.optim.Adam(log.parameters(), lr=self.lr)
            log.train()
            for iter_ in range(self.epoch):
                opt.zero_grad()
                train_logits = log(train_embs)
                train_loss = self.bce(train_logits, train_labels)
                train_loss.backward()
                opt.step()
            log.eval()
            with torch.no_grad():
                test_logits = log(test_embs)
        elif flag == "e2e":
            test_logits = embedding[idx_test]

        test_loss = self.bce(test_logits, test_lbls)
        test_preds = (torch.sigmoid(test_logits) > 0.5).float()
        test_f1_macro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='macro')
        test_f1_micro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='micro')

        return test_loss, test_f1_macro, test_f1_micro
    

    def node_classification_single_label(self, flag, embedding, idx_train, idx_test, labels):
        test_lbls = torch.argmax(labels[idx_test], dim=1)
        if flag == "ss":
            train_embs = embedding[idx_train]
            test_embs = embedding[idx_test]
            nb_classes = labels.shape[1]
            train_lbls = torch.argmax(labels[idx_train], dim=1)
            log = LogReg(train_embs.shape[1], nb_classes).to(labels.device)
            opt = torch.optim.Adam(log.parameters(), lr=self.lr)
            log.train()
            for iter_ in range(self.epoch):
                opt.zero_grad()
                train_logits = log(train_embs)
                train_loss = self.xent(train_logits, train_lbls)
                train_loss.backward()
                opt.step()
            log.eval()
            with torch.no_grad():
                test_logits = log(test_embs)
        elif flag == "e2e":
            test_logits = embedding[idx_test]

        test_loss = self.xent(test_logits, test_lbls)
        test_preds = torch.argmax(test_logits, dim=1)
        test_f1_macro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='macro')
        test_f1_micro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='micro')

        return test_loss, test_f1_macro, test_f1_micro
    

    def node_clustering(self, embedding, labels, idx_test):
        test_embs = embedding[idx_test]
        test_lbls = torch.argmax(labels[idx_test], dim=1)
        nb_classes = labels.shape[1]

        # Node Clustering Metrics
        test_embs = np.array(test_embs.cpu())
        test_lbls = np.array(test_lbls.cpu())
        accs, nmis, aris = run_kmeans(test_embs, test_lbls, nb_classes)
        sims = run_similarity_search(test_embs, test_lbls)
        return np.mean(accs), np.mean(nmis), np.mean(aris), sims

    '''
    def evaluate_mgtf(self, embedding, logits, labels, flag):
        nb_classes = labels.shape[1]
        test_embs = embedding
        test_logits = logits
        test_lbls = torch.argmax(labels, dim=1)
        with torch.no_grad():
            test_loss = self.xent(test_logits, test_lbls)

        if flag == 'test':
            # Node Classification Metrics
            test_preds = torch.argmax(test_logits, dim=1)
            test_f1_macro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='macro')
            test_f1_micro = metrics.f1_score(test_lbls.cpu(), test_preds.cpu(), average='micro')
            # Node Clustering Metrics
            test_embs = np.array(test_embs.cpu())
            test_lbls = np.array(test_lbls.cpu())
            accs, nmis, aris = run_kmeans(test_embs, test_lbls, nb_classes)
            sims = run_similarity_search(test_embs, test_lbls)
            res = {'macro_f1': test_f1_macro, 'micro_f1': test_f1_micro, 'acc': np.mean(accs), 'nmi': np.mean(nmis), 'ari': np.mean(aris), 'sims': sims}
        elif flag == 'val':
            res = {}
        return test_loss, res
    '''
    

def run_similarity_search(test_embs, test_lbls):
    numRows = test_embs.shape[0]

    cos_sim_array = metrics.pairwise.cosine_similarity(test_embs) - np.eye(numRows)
    st = []
    for N in [5, 10, 20, 50, 100]:
        indices = np.argsort(cos_sim_array, axis=1)[:, -N:]
        tmp = np.tile(test_lbls, (numRows, 1))
        selected_label = tmp[np.repeat(np.arange(numRows), N), indices.ravel()].reshape(numRows, N)
        original_label = np.repeat(test_lbls, N).reshape(numRows,N)
        st.append(str(np.round(np.mean(np.sum((selected_label == original_label), 1) / N), 4)))

    st = ','.join(st)
    return st


def run_kmeans(x, y, k):
    estimator = KMeans(n_clusters=k, n_init="auto")
    acc_list = []
    nmi_list = []
    ari_list = []
    for i in range(10):
        estimator.fit(x)
        y_pred = estimator.predict(x)
        cm = clustering_metrics(y, y_pred)
        acc, nmi, ari = cm.evaluationClusterModelFromLabel()
        acc_list.append(acc)
        nmi_list.append(nmi)
        ari_list.append(ari)

    return acc_list, nmi_list, ari_list

class clustering_metrics():
    "from https://github.com/Ruiqi-Hu/ARGA"
    def __init__(self, true_label, predict_label):
        self.true_label = true_label
        self.pred_label = predict_label


    def clusteringAcc(self):
        # best mapping between true_label and predict label
        l1 = list(set(self.true_label))
        numclass1 = len(l1)

        l2 = list(set(self.pred_label))
        numclass2 = len(l2)
        if numclass1 != numclass2:
            print('Class Not equal, Error!!!!')
            return 0

        cost = np.zeros((numclass1, numclass2), dtype=int)
        for i, c1 in enumerate(l1):
            mps = [i1 for i1, e1 in enumerate(self.true_label) if e1 == c1]
            for j, c2 in enumerate(l2):
                mps_d = [i1 for i1 in mps if self.pred_label[i1] == c2]
                cost[i][j] = len(mps_d)

        # match two clustering results by Munkres algorithm
        m = Munkres()
        cost = cost.__neg__().tolist()
        indexes = m.compute(cost)

        # get the match results
        new_predict = np.zeros(len(self.pred_label))
        for i, c in enumerate(l1):
            # correponding label in l2:
            c2 = l2[indexes[i][1]]

            # ai is the index with label==c2 in the pred_label list
            ai = [ind for ind, elm in enumerate(self.pred_label) if elm == c2]
            new_predict[ai] = c

        acc = metrics.accuracy_score(self.true_label, new_predict)
        f1_macro = metrics.f1_score(self.true_label, new_predict, average='macro')
        precision_macro = metrics.precision_score(self.true_label, new_predict, average='macro')
        recall_macro = metrics.recall_score(self.true_label, new_predict, average='macro')
        f1_micro = metrics.f1_score(self.true_label, new_predict, average='micro')
        precision_micro = metrics.precision_score(self.true_label, new_predict, average='micro')
        recall_micro = metrics.recall_score(self.true_label, new_predict, average='micro')
        return acc, f1_macro, precision_macro, recall_macro, f1_micro, precision_micro, recall_micro


    def evaluationClusterModelFromLabel(self):
        acc, f1_macro, precision_macro, recall_macro, f1_micro, precision_micro, recall_micro = self.clusteringAcc()
        nmi = metrics.normalized_mutual_info_score(self.true_label, self.pred_label)
        ari = metrics.adjusted_rand_score(self.true_label, self.pred_label)

        return acc, nmi, ari
    
