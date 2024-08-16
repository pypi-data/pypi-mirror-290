import os
import torch
import torch.nn as nn
import numpy as np
import random as random
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt



def printConfig(args):
    arg2value = {}
    for arg in vars(args):
        arg2value[arg] = getattr(args, arg)
    print(arg2value)


def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def initialize_weights(m):
    if hasattr(m, 'weight') and m.weight.dim() > 1:
        nn.init.kaiming_uniform_(m.weight.data)


def mkdir_p(path, log=True):
    """Create a directory for the specified path.
    Parameters
    ----------
    path : str
        Path name
    log : bool
        Whether to print result for directory creation
    """
    import errno
    if os.path.exists(path):
        return
    # print(path)
    # path = path.replace('\ ',' ')
    # print(path)
    try:
        os.makedirs(path)
        if log:
            print('Created directory {}'.format(path))
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path) and log:
            print('Directory {} already exists.'.format(path))
        else:
            raise


def get_dir_of_file(f_name):
    return os.path.dirname(f_name) + '/'


def init_path(dir_or_file):
    path = get_dir_of_file(dir_or_file)
    if not os.path.exists(path):
        mkdir_p(path)
    return dir_or_file


class EarlyStopping():
    def __init__(self, patience=10, path='es_checkpoint.pt'):
        self.patience = patience
        self.counter = 0
        self.best_score = None
        self.best_epoch = None
        self.early_stop = False
        if isinstance(path, list):
            self.path = [init_path(p) for p in path]
        else:
            self.path = init_path(path)

    def step(self, loss, model, epoch):
        score = loss
        if self.best_score is None:
            self.best_score = score
            self.best_epoch = epoch
            self.save_checkpoint(model)
        elif score > self.best_score:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.best_epoch = epoch
            self.save_checkpoint(model)
            self.counter = 0
        es_str = f'{self.counter:02d}/{self.patience:02d} | BestVal={self.best_score:.4f}@E{self.best_epoch}'
        return self.early_stop, es_str

    def save_checkpoint(self, model):
        """Saves model when validation loss decrease."""
        if isinstance(model, list):
            for i, m in enumerate(model):
                torch.save(m.state_dict(), self.path[i])
        else:
            torch.save(model.state_dict(), self.path)


def plot_tsne(embedding, labels, dataset_name, model_name):
    embedding = embedding.cpu().numpy()
    labels = labels.cpu().numpy()
    num_classes = labels.shape[1]
    tsne = TSNE()
    embedding_tsne = tsne.fit_transform(embedding)
    plt.figure(figsize=(10, 8))
    for class_index in range(num_classes):
        mask = (labels[:, class_index] == 1)
        plt.scatter(embedding_tsne[mask, 0], embedding_tsne[mask, 1], label=f'Class {class_index}', alpha=0.7)
    # Set all spines invisible
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Remove x and y labels
    plt.xticks([])
    plt.yticks([])
    plt.legend()#.set_visible(False)
    plt.tight_layout()
    plt.savefig(f"./tsne/{dataset_name}-{model_name}.png")
    plt.close()
