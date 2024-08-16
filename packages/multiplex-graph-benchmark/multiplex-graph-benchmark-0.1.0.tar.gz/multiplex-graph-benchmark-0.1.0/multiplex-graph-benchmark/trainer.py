import torch
from torch.utils.data import DataLoader, Subset
import time
from tqdm import tqdm
import random as random

from .utils.utils import EarlyStopping, set_seed, plot_tsne
from .utils.data_process import Dataset
from .utils.evaluator import Evaluator
from .config import print_cfg

class Trainer():
    def __init__(self, cfg):
        set_seed(cfg.seed)
        # Init args
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")
        self.dataset_name = cfg.dataset_name
        self.model_name = cfg.model_name
        self.lr = cfg.lr
        self.weight_decay = cfg.weight_decay
        self.epochs = cfg.epochs
        self.patience = cfg.patience
        self.use_batch = cfg.use_batch

        # Init Data
        self.data = Dataset(cfg)
        if cfg.use_batch:  ### ONLY used by MG-tf
            self.train_loader = DataLoader(Subset(self.data, self.data.idx_train), batch_size=cfg.dataset.batch_size, shuffle=False)
            self.val_loader = DataLoader(Subset(self.data, self.data.idx_val), batch_size=cfg.dataset.batch_size, shuffle=False)
            self.test_loader = DataLoader(Subset(self.data, self.data.idx_test), batch_size=cfg.dataset.batch_size, shuffle=False)
            self.all_loader = DataLoader(self.data, batch_size=cfg.dataset.batch_size, shuffle=False)

        # Init Model
        if self.model_name.lower() == "gcn":
            from models import GCN
            self.model = GCN(cfg).to(self.device)
        elif self.model_name.lower() == "gat":
            from models import GAT
            self.model = GAT(cfg).to(self.device)
        elif self.model_name.lower() == "mne":
            from models import MNE
            self.model = MNE(cfg).to(self.device)
        elif self.model_name.lower() == "han":
            from models import HAN
            self.model = HAN(cfg).to(self.device)
        elif self.model_name.lower() == "dmgi":
            from models import DMGI
            self.model = DMGI(cfg).to(self.device)
        elif self.model_name.lower() == "hdmi":
            from models import HDMI
            self.model = HDMI(cfg).to(self.device)
        elif self.model_name.lower() == "heco":
            from models import Heco
            self.model = Heco(cfg).to(self.device)
        elif self.model_name.lower() == 'mcgc':
            from models import MCGC
            self.model = MCGC(cfg).to(self.device)
        elif self.model_name.lower() == 'ckd':
            from models import CKD
            self.model = CKD(cfg).to(self.device)
        elif self.model_name.lower() == 'mgdcr':
            from models import MGDCR
            self.model = MGDCR(cfg).to(self.device)
        elif self.model_name.lower() == 'dmg':
            from models import DMG
            self.model = DMG(cfg).to(self.device)
        elif self.model_name.lower() == 'mgtf':
            from models import MGtf
            self.model = MGtf(cfg).to(self.device)
        else:
            raise NotImplementedError("Unknown Model!")
        
        # Init Optimizer 
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        # Init Evaluater
        self.evaluator = Evaluator(cfg.test_epochs, cfg.test_lr, cfg.test_iterater)
        # Init EarlyStop
        self.ckpt = f"./saved_model/{self.model_name.lower()}_{self.dataset_name.lower()}.pt"
        self.stopper = EarlyStopping(patience=cfg.patience, path=self.ckpt)if cfg.patience > 0 else None

        self.model.preprocess(self.data)

        # print_cfg(cfg)
        cfg.freeze()
        

    def _node_task(self):
        self.model.eval()
        labels = self.data.labels
        idx_train = self.data.idx_train
        idx_test = self.data.idx_test 
        if self.model_name.lower() in ['gcn','gat','han']:
            embedding, logits = self.model.get_embedding(self.data)
            embedding_classification = logits
            embedding_clustering = embedding
            flag = "e2e"
        elif self.model_name.lower() == 'mgtf':
            embedding, logits, labels = self.model.get_embedding(self.all_loader)
            embedding_classification = logits
            embedding_clustering = embedding
            flag = "e2e"
        else:
            embedding = self.model.get_embedding(self.data)
            embedding_classification = embedding
            embedding_clustering = embedding
            flag = "ss"

        plot_tsne(embedding[idx_test], labels[idx_test], self.dataset_name, self.model_name)
        if self.dataset_name == "imdb2":
            _, f1_macro, f1_micro = self.evaluator.node_classification_multi_label(flag, embedding_classification, idx_train, idx_test, labels)
        else:
            _, f1_macro, f1_micro = self.evaluator.node_classification_single_label(flag, embedding_classification, idx_train, idx_test, labels)
        acc, nmi, ari, sim = self.evaluator.node_clustering(embedding_clustering, labels, idx_test)
        return f1_macro, f1_micro, acc, nmi, ari, sim
        

    def _edge_classification(self):
        self.model.eval()
        edge_idx_train = self.data.edge_idx_train['classification']
        edge_idx_test = self.data.edge_idx_test['classification']
        edge_labels = self.data.edge_labels['classification']

        edge_index_list = self.data.edge_index_list
        if self.model_name.lower() in ['gcn','gat','han']:
            embedding, _ = self.model.get_embedding(self.data)
        elif self.model_name.lower() == 'mgtf':
            embedding, _, _ = self.model.get_embedding(self.all_loader)
        else:
            embedding = self.model.get_embedding(self.data)
        ec_acc, ec_f1 = self.evaluator.edge_classification(embedding, edge_index_list, edge_labels, edge_idx_train, edge_idx_test)

        return ec_acc, ec_f1
    

    def _edge_prediction(self):
        self.model.eval()
        edge_idx_train = self.data.edge_idx_train['prediction']
        edge_idx_test = self.data.edge_idx_test['prediction']
        edge_labels = self.data.edge_labels['prediction']

        if self.model_name.lower() in ['gcn','gat','han']:
            embedding, _ = self.model.get_embedding(self.data)
        elif self.model_name.lower() == 'mgtf':
            embedding, _, _ = self.model.get_embedding(self.all_loader)
        else:
            embedding = self.model.get_embedding(self.data)
        ep_aucroc, ep_aucpr, ep_f1, ep_mrr = self.evaluator.edge_prediction(embedding, edge_idx_train, edge_idx_test, edge_labels)

        return ep_aucroc, ep_aucpr, ep_f1, ep_mrr
    

    def train(self):
        print("Started training...") 
        start = time.time()   
        for epoch in range(self.epochs):
            ### Train
            self.model.train()
            if self.model_name.lower() == 'mgtf':
                total_loss = 0.0
                for batch_input in self.train_loader:
                    self.optimizer.zero_grad()
                    loss = self.model(batch_input)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                    self.optimizer.step()
                    total_loss += loss.item()
                train_loss = total_loss / len(self.train_loader)
            elif self.model_name.lower() in ['dmg','ckd']:
                loss = self.model(self.data, self.optimizer, epoch)
                train_loss = loss.item()
            else:
                self.optimizer.zero_grad()
                loss = self.model(self.data)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                self.optimizer.step()
                train_loss = loss.item()

            ### Validate
            self.model.eval()
            with torch.no_grad():
                ### TBD
                val_loss = train_loss

            if self.stopper is not None:
                es_flag, es_str = self.stopper.step(val_loss, self.model, epoch)
                if es_flag:
                    break
        end = time.time()
        print(f'Train time per epoch: {(1000*(end-start)/self.epochs):.2f} ms')
        self.model.postprocess(self.data)
        if self.stopper is not None:
            self.model.load_state_dict(torch.load(self.stopper.path))
        return self.model
    

    def eval_and_save(self):
        print("Started evaluating...")   
        torch.save(self.model.state_dict(), self.ckpt)
        self.model.eval()

        res = {}
        f1_macro, f1_micro, acc, nmi, ari, sim  = self._node_task()
        ec_acc, ec_f1 = self._edge_classification()
        ep_aucroc, ep_aucpr, ep_f1, ep_mrr = self._edge_prediction()

        res['macro_f1'] = f1_macro
        res['micro_f1'] = f1_micro
        res['acc'] = acc
        res['nmi'] = nmi
        res['ari'] = ari
        res['sims'] = sim
        res['ec_acc'] = ec_acc
        res['ec_f1'] = ec_f1
        res['ep_aucroc'] = ep_aucroc
        res['ep_aucpr'] = ep_aucpr
        res['ep_f1'] = ep_f1
        res['ep_mrr'] = ep_mrr
        return res