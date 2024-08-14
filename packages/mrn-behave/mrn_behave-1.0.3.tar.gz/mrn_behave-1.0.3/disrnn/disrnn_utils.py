from data.data_utils import load_master_dataset, load_split
import torch
from torch import Tensor
from torch.utils.data import Dataset
import numpy as np
from torch.nn.utils.rnn import pad_sequence

class DisRNNDataset(Dataset):
    def __init__(self, subject: str, split: str, fold: int) -> None:
        super().__init__()
        full_dataset = load_master_dataset(subject)
        self.split = split
        self.fold = load_split(subject, fold)
        self.sessions = self.fold[split]
        self.dataset = list(filter(lambda x: x['session_id'] in self.sessions, full_dataset))

        self.length = sum(map(lambda x: len(x['y']), self.dataset))
        self.c_stim_trials = sum(map(lambda x: np.sum(x['X'][1:, 0] == 0), self.dataset))
        self.o_stim_trials = sum(map(lambda x: np.sum(x['X'][1:, 0] != 0), self.dataset))
        self.error_trials = sum(map(lambda x: np.sum(x['X'][1:, 2] == 0), self.dataset))

    def __getitem__(self, index) -> Tensor:

        session = self.dataset[index]
        X, y = session['X'], session['y'][1:]
        y[y == -1] = 0

        return torch.from_numpy(X), torch.from_numpy(y)
    
    def __len__(self) -> int:
        return len(self.dataset)
    

def count_entries(d):
    return np.sum(d['X'][:, 0] == 0)