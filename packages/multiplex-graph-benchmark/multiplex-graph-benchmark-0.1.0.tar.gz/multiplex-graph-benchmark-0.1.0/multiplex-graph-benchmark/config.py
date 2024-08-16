import os
import argparse
from yacs.config import CfgNode as CN
from itertools import product

def print_cfg(cfg): 
    print("Train Config:")
    for key, value in cfg.items():
        if not isinstance(value, CN):
            print(f"  {key}: {value}")

    # print("Dataset Config:")
    # for key, value in cfg.dataset.items():
    #     print(f"  {key}: {value}")

    if cfg.model_name in ['gcn', 'gat']:
        print("GNN Config:")
        for key, value in cfg.gnn.items():
            print(f"  {key}: {value}")
    else:
        print(f"{cfg.model_name} Config:")
        for key, value in cfg[cfg.model_name].items():
            print(f"  {key}: {value}")

def set_cfg(cfg):
    # ------------------------------------------------------------------------ #
    # Basic options
    # ------------------------------------------------------------------------ #
    cfg.dataset_name = ''
    cfg.model_name = ''
    cfg.gpu_num = 0
    # cfg.seed = [0,1,2,3,4]
    cfg.seed = [0]
    cfg.runs = 4
    cfg.lr = 1e-3
    cfg.weight_decay = 1e-4
    cfg.epochs = 200
    cfg.patience = 20
    cfg.test_epochs = 200
    cfg.test_lr = 0.1
    cfg.test_iterater = 10
    cfg.use_batch = False

    cfg.dataset = CN()
    cfg.gnn = CN()
    cfg.mne = CN()
    cfg.han = CN()
    cfg.dmgi = CN()
    cfg.hdmi = CN()
    cfg.heco = CN()
    cfg.mcgc = CN()
    cfg.ckd = CN()
    cfg.mgdcr = CN()
    cfg.dmg = CN()
    cfg.mgtf = CN()

    cfg.dataset.root = './data/'
    cfg.dataset.sc = 1
    cfg.dataset.sparse = False
    cfg.dataset.nb_nodes = 0
    cfg.dataset.nb_classes = 0
    cfg.dataset.ft_size = 0
    cfg.dataset.num_view = 0
    cfg.dataset.batch_size = 64

    cfg.gnn.hidden_dim = 64
    cfg.gnn.layers = 2
    cfg.gnn.dropout = 0.1
    cfg.gnn.isBias = True
    cfg.gnn.activation = 'relu'


     # ------------------------------------------------------------------------ #
    # MGtf(ours) Model options
    # ------------------------------------------------------------------------ #
    cfg.mgtf.seq_len = 0
    cfg.mgtf.aggregator = ''
    cfg.mgtf.lap_dim = 0
    cfg.mgtf.beta = 0.0
    cfg.mgtf.p = 0
    cfg.mgtf.normalization = ''
    cfg.mgtf.zero_diag = False
    cfg.mgtf.d_model = 0
    cfg.mgtf.ffn_hidden = 0
    cfg.mgtf.attn_heads = 0
    cfg.mgtf.encoder_layers = 0
    cfg.mgtf.dropout = 0.0

    # ------------------------------------------------------------------------ #
    # MNE Model options
    # ------------------------------------------------------------------------ #
    cfg.mne.p = 0.0
    cfg.mne.q = 0.0
    cfg.mne.walk_length = 0
    cfg.mne.context_size = 0
    cfg.mne.walks_per_node = 0
    cfg.mne.num_negative_samples = 0

    # ------------------------------------------------------------------------ #
    # DMGI Model options
    # ------------------------------------------------------------------------ #
    cfg.dmgi.reg_coef = 0.0
    cfg.dmgi.sup_coef = 0.0
    cfg.dmgi.margin = 0.0
    cfg.dmgi.nheads = 0
    cfg.dmgi.isSemi = False
    cfg.dmgi.isAttn = False


    # ------------------------------------------------------------------------ #
    # HDMI Model options
    # ------------------------------------------------------------------------ #
    cfg.hdmi.coef_layers = [0]
    cfg.hdmi.coef_fusion = [0]
    cfg.hdmi.same_discriminator = False


    # ------------------------------------------------------------------------ #
    # MCGC Model options
    # ------------------------------------------------------------------------ #
    cfg.mcgc.alpha = 0.0
    cfg.mcgc.gama = 0.0

    # ------------------------------------------------------------------------ #
    # Heco Model options
    # ------------------------------------------------------------------------ #
    cfg.heco.tau = 0.0
    cfg.heco.lam = 0.0
    cfg.heco.feat_drop = 0.0
    cfg.heco.attn_drop = 0.0
    cfg.heco.sample_rate = [0]
    cfg.heco.nei_num = 0
    cfg.heco.type_num = [0]
    cfg.heco.pos_num = 0
    cfg.heco.feats_dim_list = [0]


    # ------------------------------------------------------------------------ #
    # CKD Model options
    # ------------------------------------------------------------------------ #
    cfg.ckd.negative_cnt = 0
    cfg.ckd.topk = 0
    cfg.ckd.sample_times = 0
    cfg.ckd.neigh_por = 0.0
    cfg.ckd.global_weight = 0.0
    cfg.ckd.batch_size = 0


    # ------------------------------------------------------------------------ #
    # DMG Model options
    # ------------------------------------------------------------------------ #
    cfg.dmg.c_dim = 0
    cfg.dmg.p_dim = 0
    cfg.dmg.phi_hidden_size = 0
    cfg.dmg.phi_num_layers = 0
    cfg.dmg.alpha = 0.0
    cfg.dmg.beta = 0.0
    cfg.dmg.lammbda = 0.0
    cfg.dmg.feature_drop = 0.0
    cfg.dmg.neighbor_num = 0
    cfg.dmg.sample_neighbor = 0
    cfg.dmg.sample_num = 0
    cfg.dmg.decolayer = 0
    cfg.dmg.inner_epochs = 0
    cfg.dmg.tau = 0.0
    
    # ------------------------------------------------------------------------ #
    # MGDCR Model options
    # ------------------------------------------------------------------------ #
    cfg.mgdcr.lambdintra = [0.0]
    cfg.mgdcr.lambdinter = [0.0]
    cfg.mgdcr.w_intra = [0.0]
    cfg.mgdcr.w_inter = [0.0]
    cfg.mgdcr.mlp_cfg = [0]


    return cfg

def update_cfg(cfg, args_str=None):
    parser = argparse.ArgumentParser()
    # opts arg needs to match set_cfg
    parser.add_argument("opts", default=[], nargs=argparse.REMAINDER, help="Modify config options using the command-line")

    if isinstance(args_str, str):
        # parse from a string
        args = parser.parse_args(args_str.split())
    else:
        # parse from command line
        args = parser.parse_args()
    # Clone the original cfg
    cfg = cfg.clone()

    # Update from command line
    cfg.merge_from_list(args.opts)

    #Update from config file
    config_path = f"./yamls/{cfg.model_name.lower()}.yaml"
    if os.path.isfile(config_path):
        model_cfg = CN.load_cfg(open(config_path, 'r'))
    else:
        raise FileNotFoundError(f"Model-specific config file not found: {config_path}")
    model_dataset_cfg = getattr(model_cfg, cfg.dataset_name.lower(), None)
    if model_dataset_cfg is None:
        raise KeyError(f"Dataset section '{cfg.dataset_name.lower()}' not found in the model's config file")
    
    ### Raw
    # cfg.merge_from_other_cfg(model_dataset_cfg)
    # return cfg


    ### Grid Search
    # Flatten the nested dictionary
    def flatten_dict(d, parent_key='', sep=','):
        items = []
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    # Flatten the nested dictionary
    flat_model_dataset_cfg = flatten_dict(model_dataset_cfg)

    # Hyperparameter grid search
    grid_search_params = []
    for key, values in flat_model_dataset_cfg.items():
        if isinstance(values, list):
            grid_search_params.append((key,values))
        else:
            grid_search_params.append((key, [values]))

    # Generate combinations for grid search
    grid_combinations = product(*[values for _, values in grid_search_params])

    # Perform grid search
    cfg_list = []
    for combination in grid_combinations:
        cfg_copy = cfg.clone()
        # Update the config directly
        for param, value in zip([param for param, _ in grid_search_params], combination):
            keys = param.split(',')
            current_dict = cfg_copy
            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})
            current_dict[keys[-1]] = value
        cfg_list.append(cfg_copy)
    return cfg_list

"""
    Global variable
"""
cfg = set_cfg(CN())