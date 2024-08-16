import os
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import scipy.io as sio
from transformers import (
    AutoTokenizer,
    AutoModel,
    LlamaForCausalLM,
    LlamaTokenizer,
    LlamaModel,
    LlamaConfig,
)
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.exceptions import NotFittedError


class SentenceDataset(Dataset):
    def __init__(self, sentences):
        self.sentences = sentences

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        return self.sentences[idx]

class SentenceEncoder:
    def __init__(self, name, corpus=None, device="cuda:0"):
        self.device = device
        self.name = name

        if name == "minilm":
            model_path = "/home1/gjh/LM_models/all-MiniLM-L6-v2" #384
            # model_path = 'sentence-transformers/all-MiniLM-L6-v2'
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, device=self.device)
            self.model = AutoModel.from_pretrained(model_path).to(self.device)
        elif name == "mpnet-base":
            model_path = "/home1/gjh/LM_models/all-mpnet-base-v2" #768
            # model_path = 'sentence-transformers/all-mpnet-base-v2'
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, device=self.device)
            self.model = AutoModel.from_pretrained(model_path).to(self.device)
        elif name == "roberta-large":
            model_path = "/home1/gjh/LM_models/all-roberta-large-v1" #1024
            # model_path = 'sentence-transformers/all-roberta-large-v1'
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, device=self.device)
            self.model = AutoModel.from_pretrained(model_path).to(self.device)
        elif name == "bow":
            self.vectorizer = CountVectorizer()  # or TfidfVectorizer() if you prefer TF-IDF
            if corpus is not None:
                print("Fitting corpus...")
                self.vectorizer.fit(corpus)
            else:
                raise ValueError("A corpus must be provided to fit the vectorizer when using BoW.")
        else:
            raise ValueError(f"Unknown language model: {name}.")

    def encode_batch(self, batch_texts):
        if self.name == "bow":
            try:
                return torch.tensor(self.vectorizer.transform(batch_texts).toarray()).float()
            except NotFittedError:
                raise ValueError("The vectorizer has not been fitted. Please fit it on a corpus first.")
        
        encoded_input = self.tokenizer(batch_texts, padding=True, return_tensors='pt').to("cuda")
        self.model.eval()
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings

    def encode(self, dataloader):
        all_embeddings = []
        for batch_texts in tqdm(dataloader):
            batch_texts = list(batch_texts)
            embeddings = self.encode_batch(batch_texts)
            all_embeddings.append(embeddings)
        return torch.cat(all_embeddings, dim=0)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def main(data_name, encoder):
    ### load raw text
    raw_file_path = f'./{data_name}/raw/{data_name}_text_abl3.mat'
    save_file_path = f'./{data_name}/raw/{data_name}_vec_abl3.mat'
    mat_contents = sio.loadmat(raw_file_path)
    feature_text = mat_contents['feature_text']
    feature_text_lst = []
    for ft in feature_text[0]:
        feature_text_lst.append(str(ft))

    ### embedding
    encoder = SentenceEncoder(name=encoder, corpus=feature_text_lst[:200])
    # answer_texts_squeeze = [answer_text[0] for answer_text in answer_texts]
    # answer_texts_squeeze = DataLoader(SentenceDataset(answer_texts_squeeze), batch_size=64, shuffle=False, num_workers=4)
    # embedding = encoder.encode(answer_texts_squeeze)
    raw_text = DataLoader(SentenceDataset(feature_text_lst), batch_size=64, shuffle=False, num_workers=4)
    raw_embedding = encoder.encode(raw_text)

    ### save embeddings to .mat file
    mat_contents['feature'] = raw_embedding.cpu().numpy()
    print(mat_contents['feature'].shape)
    del mat_contents['feature_text']
    sio.savemat(save_file_path, mat_contents)


if __name__ == '__main__':
    main(data_name='amazon2', encoder='mpnet-base')