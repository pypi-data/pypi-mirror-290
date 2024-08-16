import scipy.io
import numpy as np

def see(mat_file_path):
    print(mat_file_path)
    mat_contents = scipy.io.loadmat(mat_file_path)

    for i, (key, value) in enumerate(mat_contents.items()):
        if not key.startswith('__'):
            if isinstance(value, scipy.sparse._csc.csc_matrix):
                print(f"{key}, {value.shape}, edges: {value.nnz}, density: {value.nnz / (value.shape[0]*value.shape[1])}, {type(value)}")
            else:
                print(f"{key}, {value.shape}, {type(value)}")

    if 'label' in mat_contents.keys():
        one_hot_labels = mat_contents['label']
        arg_labels = np.argmax(one_hot_labels,1)
        unique, counts = np.unique(arg_labels, return_counts=True)
        print("Label: {}".format({un:cn for un, cn in zip(unique, counts)}))

    if 'feature_text' in mat_contents.keys():
        print(mat_contents['feature_text'][:,0])

    print("\n\n")


# see('./acm2/raw/acm2_text.mat')
# see('./acm2/raw/acm2_vec.mat')
# see('./acm/raw/ACM3025.mat')

# see('./imdb2/raw/imdb2_text.mat')
# see('./imdb2/raw/imdb2_vec.mat')
# see('./imdb/raw/IMDB4780.mat')

# see('./dblp2/raw/dblp2_text.mat')
# see('./dblp2/raw/dblp2_vec.mat')
# see('./dblp/raw/DBLP4057.mat')

# see('./amazon2/raw/amazon2_text.mat')
# see('./amazon2/raw/amazon2_vec.mat')
# see('./amazon/raw/AMAZON7621.pkl')

# see('./amazon_fraud/raw/Amazon_fraud.mat')
# see('./yelpchi_fraud/raw/YelpChi_fraud.mat')

