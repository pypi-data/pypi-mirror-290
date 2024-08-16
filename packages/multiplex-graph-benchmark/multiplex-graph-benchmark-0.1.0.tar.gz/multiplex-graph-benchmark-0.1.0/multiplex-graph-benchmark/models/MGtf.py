import torch
import torch.nn as nn
import numpy as np
import random as random
from sklearn import metrics

from models.MGtf_utils import  MLP, GNN, TransformerEncoder, AGGRCODINGS
from models.pos_encoding import DiffusionEncoding, PStepRWEncoding, LapEncoding
from utils.utils import initialize_weights
from utils.evaluator import run_kmeans, run_similarity_search


class MGtf(nn.Module):
    def __init__(self, cfg):
        super(MGtf, self).__init__()
        self.args = cfg
        gpu_num_ = cfg.gpu_num
        if gpu_num_ == -1:
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda:" + str(gpu_num_) if torch.cuda.is_available() else "cpu")

        self.tf_encoders = nn.ModuleList([TransformerEncoder(input_dim=cfg.dataset.ft_size+cfg.mgtf.lap_dim,
                                              d_model=cfg.mgtf.d_model, 
                                              ffn_hidden=cfg.mgtf.ffn_hidden,
                                              n_head=cfg.mgtf.attn_heads, 
                                              n_layers=cfg.mgtf.encoder_layers,
                                              drop_prob=cfg.mgtf.dropout)
                                            for _ in range(cfg.dataset.num_view)]).to(self.device)
        aggregate_method = AGGRCODINGS.get(cfg.mgtf.aggregator, None)
        if cfg.mgtf.aggregator == 'attn':
            aggr_params = {'input_dim':cfg.mgtf.d_model, 'layers':cfg.dataset.num_view}
        elif cfg.mgtf.aggregator == 'transformer':
            aggr_params = {'input_dim':cfg.mgtf.d_model, 'd_model':cfg.mgtf.d_model, 'ffn_hidden':cfg.mgtf.ffn_hidden,
                        'n_head':1, 'n_layers':2, 'drop_prob':cfg.mgtf.dropout}
        else:
            aggr_params = {}
        self.aggregator = aggregate_method(**aggr_params).apply(initialize_weights).to(self.device) 
        self.mlp_cls = MLP(cfg.mgtf.d_model, [100,50], cfg.dataset.nb_classes, cfg.mgtf.dropout).apply(initialize_weights).to(self.device)
        self.criterion = nn.CrossEntropyLoss()

        self.init_weight()

    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.fill_(0.0) 

    def forward(self, batch):
        batch_inputs, batch_attentions, batch_masks, batch_labels = batch
        batch_inputs = batch_inputs.permute(1,0,2,3)         #[view,B,seq,dim]<--[B,view,seq,dim]
        batch_attentions = batch_attentions.permute(1,0,2,3) #[view,B,seq,seq]<--[B,view,seq,seq]
        batch_masks = batch_masks.permute(1,0,2)             #[view,B,seq]    <--[B,view,seq]
        hiddens = []
        for view in range(self.args.dataset.num_view):
            hidden = self.tf_encoders[view](batch_inputs[view], batch_attentions[view], batch_masks[view])   #[B,dim]<--[B,seq,dim]
            hiddens.append(hidden)
        agg_hidden = self.aggregator(hiddens)                     #[B,dim]<--[view,B,dim]
        out = self.mlp_cls(agg_hidden)                            #[B,cls]<--[B,dim]
        loss = self.criterion(out, batch_labels)
        return loss
    
    def get_embedding(self, data_loader):
        all_predictions = []
        all_labels = []
        all_hiddens = []
        with torch.no_grad():
            for batch_inputs, batch_attentions, batch_masks, batch_labels in data_loader:
                batch_inputs = batch_inputs.permute(1,0,2,3)
                batch_attentions = batch_attentions.permute(1,0,2,3)
                batch_masks = batch_masks.permute(1,0,2)
                hiddens = []
                # print(torch.isnan(batch_inputs).any(),torch.isnan(batch_attentions).any(),torch.isnan(batch_masks).any())
                for view in range(self.args.dataset.num_view):
                    hidden = self.tf_encoders[view](batch_inputs[view], batch_attentions[view], batch_masks[view])
                    # print(torch.isnan(hidden).any()) #这里产生了nan
                    hiddens.append(hidden)
                agg_hidden = self.aggregator(hiddens)
                # print(torch.isnan(agg_hidden).any())
                out = self.mlp_cls(agg_hidden)
                all_hiddens.append(agg_hidden)
                all_predictions.append(out)
                all_labels.append(batch_labels)
            all_hiddens = torch.cat(all_hiddens, dim=0)
            all_predictions = torch.cat(all_predictions, dim=0)
            all_labels = torch.cat(all_labels, dim=0)
        return all_hiddens, all_predictions, all_labels

        
    def preprocess(self, data):
        # diffPE_path = f'{self.args.dataset.root}/{self.args.dataset_name}/processed/diffusion_{args.beta}_{args.normalization}.pkl'
        # diff_pos_encoder = DiffusionEncoding(savepath=diffPE_path, beta=args.beta, normalization=args.normalization)
        # diff_pos_encoder.apply_to(dataset, pe_type='rel', overwrite=False)
        
        rwPE_config = f"{self.args.mgtf.p}stepRW_{self.args.mgtf.beta}_{self.args.mgtf.normalization}"
        rwPE_path = f'{self.args.dataset.root}/{self.args.dataset_name}/processed/{rwPE_config}.pkl'
        rw_pos_encoder = PStepRWEncoding(savepath=rwPE_path, p=self.args.mgtf.p, beta=self.args.mgtf.beta, normalization=self.args.mgtf.normalization)
        rw_pos_encoder.apply_to(data, pe_type='rel', overwrite=False)

        lapPE_config = f"laplacian_{self.args.mgtf.lap_dim}_{self.args.mgtf.normalization}"
        lapPE_path =  f'{self.args.dataset.root}/{self.args.dataset_name}/processed/{lapPE_config}.pkl'
        lap_pos_encoder = LapEncoding(savepath=lapPE_path, dim=self.args.mgtf.lap_dim, normalization=self.args.mgtf.normalization)
        lap_pos_encoder.apply_to(data, pe_type='abs', overwrite=False)

        tf_input_config = f"[{self.args.mgtf.seq_len}]_[{rwPE_config}]_[{lapPE_config}]"
        tf_input_path = f'{self.args.dataset.root}/{self.args.dataset_name}/processed/{tf_input_config}.pt'
        data.update_features(path=tf_input_path, overwrite=False)

        self.args.freeze()


    def postprocess(self, data):
        pass