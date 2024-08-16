import numpy as np
import time
from tqdm import tqdm

from .config import cfg, update_cfg, print_cfg
from .trainer import Trainer
from .utils.utils import set_seed


def main(cfg):
    seeds = cfg.seed if cfg.seed is not None else range(cfg.runs)

    #Node Classification
    f1_macros = []
    f1_micros = []
    #Node Clustering
    accs = []
    nmis = []
    aris = []
    sims = []
    #Edge Classification
    ec_accs = []
    ec_f1s = []
    #Edge Prediction
    ep_aucrocs = []
    ep_aucprs = []
    ep_f1s = []
    ep_mrrs = []

    start = time.time()
    for seed in tqdm(seeds):
        set_seed(seed)
        cfg.defrost()
        cfg.seed = seed
        trainer = Trainer(cfg)
        cfg.freeze()
        trainer.train()
        res = trainer.eval_and_save()
        #node classification
        f1_macros.append(res['macro_f1'])
        f1_micros.append(res['micro_f1'])
        #node clustering
        accs.append(res['acc'])
        nmis.append(res['nmi'])
        aris.append(res['ari'])
        #edge classification
        ec_accs.append(res['ec_acc'])
        ec_f1s.append(res['ec_f1'])
        #edge prediction
        ep_aucrocs.append(res['ep_aucroc'])
        ep_aucprs.append(res['ep_aucpr'])
        ep_f1s.append(res['ep_f1'])
        ep_mrrs.append(res['ep_mrr'])

        del trainer
    end = time.time()

    print("\t[Node Classification] Macro-F1 | Micro-F1")
    print(f"\t&{(100*np.mean(f1_macros)):.2f}±{(100*np.std(f1_macros)):.1f}    &{(100*np.mean(f1_micros)):.2f}±{(100*np.std(f1_micros)):.1f}")
    print("\t[Node Clustering] ACC | NMI")
    print(f"\t&{(100*np.mean(accs)):.2f}±{(100*np.std(accs)):.1f}    &{(100*np.mean(nmis)):.2f}±{(100*np.std(nmis)):.1f}")
    print("\t[Edge Classification] ACC | F1")
    print(f"\t&{(100*np.mean(ec_accs)):.2f}±{(100*np.std(ec_accs)):.1f}    &{(100*np.mean(ec_f1s)):.2f}±{(100*np.std(ec_f1s)):.1f}")
    print("\t[Edge Prediction] AUC_ROC | AUC_PR | F1 | MRR")
    print(f"\t&{(100*np.mean(ep_aucrocs)):.2f}±{(100*np.std(ep_aucrocs)):.1f}    &{(100*np.mean(ep_aucprs)):.2f}±{(100*np.std(ep_aucprs)):.1f}    &{(100*np.mean(ep_f1s)):.2f}±{(100*np.std(ep_f1s)):.1f}   &{(100*np.mean(ep_mrrs)):.2f}±{(100*np.std(ep_mrrs)):.1f}")
    print(f"Total Running time: {(end-start)/len(seeds):.2f}s")



if __name__ == '__main__':
    ### Grid Search
    cfg_list = update_cfg(cfg)
    for cfg in cfg_list:
        # print_cfg(cfg)
        main(cfg)
