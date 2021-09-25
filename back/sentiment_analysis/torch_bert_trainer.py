import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from torch.optim import Adam
import torch.nn.functional as F

class NsmcDataset(Dataset):
    ''' Naver Sentiment Movie Corpus Dataset '''
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        text = self.df.iloc[idx, 0]
        label = self.df.iloc[idx, 1]
        return text, label

class EarlyStopping(object):
    def __init__(self, mode='min', min_delta=0, patience=10, percentage=False):
        self.mode = mode
        self.min_delta = min_delta
        self.patience = patience
        self.best = None
        self.num_bad_epochs = 0
        self.is_better = None
        self._init_is_better(mode, min_delta, percentage)

        if patience == 0:
            self.is_better = lambda a, b: True
            self.step = lambda a: False

    def step(self, metrics):
        if self.best is None:
            self.best = metrics
            return False

        if np.isnan(metrics):
            return True

        if self.is_better(metrics, self.best):
            self.num_bad_epochs = 0
            self.best = metrics
        else:
            self.num_bad_epochs += 1
            print(f"MuYaHooooooo!!!! {metrics} - {self.best} - {self.is_better(metrics, self.best)}")

        if self.num_bad_epochs >= self.patience:
            print('terminating because of early stopping!')
            return True

        return False

    def _init_is_better(self, mode, min_delta, percentage):
        if mode not in {'min', 'max'}:
            raise ValueError('mode ' + mode + ' is unknown!')
        if not percentage:
            if mode == 'min':
                self.is_better = lambda a, best: a < best - min_delta
            if mode == 'max':
                self.is_better = lambda a, best: a > best + min_delta
        else:
            if mode == 'min':
                self.is_better = lambda a, best: a < best - (best * min_delta / 100)
            if mode == 'max':
                self.is_better = lambda a, best: a > best + (best * min_delta / 100)

import os
import time
model_name_list = ['beomi/kcbert-base', 'snunlp/KR-BERT-char16424', 'dsksd/bert-ko-small-minimal', 'snunlp/KR-Medium']
more_model = []
learning_rate_list = [1e-6]*len(model_name_list)#3e-5, 5e-5, 1e-4, 3e-4
batch_size_list = [8]*len(model_name_list)#128, 64, 32,
padding_size = [300] + [512]*(len(model_name_list) - 1)

for name, lr, bs, ps in zip(model_name_list, learning_rate_list, batch_size_list, padding_size):
    start_time = time.time()
    dataset_counter = 1
    print()
    print("-" * 70)
    print(f"now {name} turn is start!!!")
    print("-" * 70)
    print()
    for dirpath, dirnames, filenames in os.walk('./dataset'):
        if len(dirnames) != 0:
            continue
        dataset_len = len(dirnames)

        dataset_name = dirpath.split('/')[-1]
        train_name = dataset_name + "_train.csv"
        test_name = dataset_name + "_test.csv"
        train_df = pd.read_csv(dirpath + "/" + train_name)
        test_df = pd.read_csv(dirpath + "/" + test_name)

        print()
        print("-" * 70)
        print(f"now {dataset_counter} : {name} - {dataset_name} is running!!!")
        print("-" * 70)
        print()

        nsmc_train_dataset = NsmcDataset(train_df)
        train_loader = DataLoader(nsmc_train_dataset, batch_size=bs, shuffle=True, num_workers=4)
        device = torch.device("cuda")
        tokenizer = BertTokenizer.from_pretrained(f'{name}')
        model = BertForSequenceClassification.from_pretrained(f'{name}')
        es = EarlyStopping(mode='max', patience=2, min_delta=0.001)
        model.to(device)

        optimizer = Adam(model.parameters(), lr=lr)
        itr = 1
        p_itr = 500
        epochs = 15
        total_loss = 0
        total_len = 0
        total_correct = 0

        model.train()
        for epoch in range(epochs):
            for text, label in train_loader:
                optimizer.zero_grad()

                # encoding and zero padding
                if name == 'beomi/kcbert-base':
                    encoded_list = [tokenizer.encode(str(t), add_special_tokens=True)[:300] for t in text]
                else:
                    encoded_list = [tokenizer.encode(str(t), add_special_tokens=True)[:512] for t in text]
                padded_list = [e + [0] * (ps - len(e)) for e in encoded_list]

                sample = torch.tensor(padded_list)
                sample, label = sample.to(device), label.to(device)
                labels = label.clone().detach()
                outputs = model(sample, labels=labels)
                loss, logits = outputs['loss'], outputs['logits']

                pred = torch.argmax(F.softmax(logits), dim=1)
                correct = pred.eq(labels)
                total_correct += correct.sum().item()
                total_len += len(labels)
                total_loss += loss.item()
                loss.backward()
                optimizer.step()

                if itr % p_itr == 0:
                    print(f'[Epoch {epoch + 1}/{epochs}] Iteration {itr} -> Train Loss: {round(total_loss / p_itr, 4)}, Accuracy: {round(total_correct / total_len, 3)}')
                    total_loss = 0
                    total_len = 0
                    total_correct = 0

                itr += 1

            # evaluation
            model.eval()

            nsmc_eval_dataset = NsmcDataset(test_df)
            eval_loader = DataLoader(nsmc_eval_dataset, batch_size=2, shuffle=False, num_workers=2)

            total_loss = 0
            total_len = 0
            total_correct = 0

            for text, label in eval_loader:
                if name == 'beomi/kcbert-base':
                    encoded_list = [tokenizer.encode(str(t), add_special_tokens=True)[:300] for t in text]
                else:
                    encoded_list = [tokenizer.encode(str(t), add_special_tokens=True)[:512] for t in text]
                padded_list = [e + [0] * (ps - len(e)) for e in encoded_list]
                sample = torch.tensor(padded_list)
                sample, label = sample.to(device), label.to(device)
                labels = torch.tensor(label)
                outputs = model(sample, labels=labels)
                _, logits = outputs['loss'], outputs['logits']

                pred = torch.argmax(F.softmax(logits), dim=1)
                correct = pred.eq(labels)
                total_correct += correct.sum().item()
                total_len += len(labels)

            print('Test accuracy: ', total_correct / total_len)
            torch.save(model.state_dict(), f'../data/{name}-{dataset_name}_model.state(epoch{epoch + 1}-{round(total_correct / total_len, 4)}).bin')
            if es.step(total_correct / total_len):
                break
            total_loss = 0
            total_len = 0
            total_correct = 0
            model.train()
        dataset_counter += 1
    print()
    print('-' * 70)
    end_time = time.time()
    print(f"running time : {int((end_time-start_time)/3600)}hour {int((end_time-start_time)%3600/60)}min {int((end_time-start_time)%60)}sec")
    print('-' * 70)
    print()