from ..data.data_utils import load_master_dataset, load_split
import torch
from torch import Tensor
import numpy as np
from torch.utils.data import Dataset
from linear_switching.linear_switching import LinearSwitching
from torch.utils.data import DataLoader
import torch.nn.functional as F


def convert_dataset(dataset: list[dict]):
    observations = {
        (-1, 1, 1) : 0,
        (0, -1, 1) : 1,
        (0, 1, 1) : 2,
        (1, -1, 1) : 3,
        (-1, -1, 0) : 4,
        (0, 1, 0) : 5,
        (0, -1, 0) : 6,
        (1, 1, 0) : 7
    }
    for session in dataset:
        X = session['X']
        session['X'] = np.array(list(map(lambda x: observations[tuple(x)], session['X'])))
    return dataset


class LinearSwitchingDataset(Dataset):
    def __init__(self, subject: str, split: str, fold: int) -> None:
        super().__init__()
        full_dataset = load_master_dataset(subject)
        self.split = split
        self.fold = load_split(subject, fold)
        self.sessions = self.fold[split]
        self.dataset = list(filter(lambda x: x['session_id'] in self.sessions, full_dataset))
        self.dataset = convert_dataset(self.dataset)

    def __getitem__(self, index) -> Tensor:
        session = self.dataset[index]
        X, y = session['X'], session['y'][1:]
        y[y == -1] = 0
        return torch.from_numpy(X), torch.from_numpy(y)
        
    def __len__(self) -> int:
        return len(self.dataset)
    

def evaluate(model: LinearSwitching, loader: DataLoader) -> dict:
    summary = {
        'total_loss' : [],
        'center_stim_loss' : [],
        'outside_stim_loss' : [],
        'total_score' : [],
        'center_stim_score' : [],
        'outside_stim_score' : [],
        'total_acc' : [],
        'center_stim_acc' : [],
        'outside_stim_acc' : []
    }
    # Data observation mapping
    left_stim = torch.tensor([0, 4])
    center_stim = torch.tensor([1, 2, 5, 6])
    right_stim = torch.tensor([3, 7])
    # Initialize metrics
    total_loss = 0
    outside_stim_loss = 0
    center_stim_loss = 0
    total_count = 0
    outside_stim_count = 0
    center_stim_count = 0
    total_correct = 0
    outside_stim_correct = 0
    center_stim_correct = 0
    probs = []
    outside_stim_probs = []
    center_stim_probs = []
    # Iterate over batches
    for (X, y, mask) in loader:

        y[y == -1] = 0
        B, T = X.shape
        cumulated_log_probs = torch.zeros(size=(B, T - 1, 2))
        z = model.z_0.expand(size=(B, 1))

        for t in range(T - 1):
            z = model(z, X[:, t])
            l_stim_trials = torch.where(torch.isin(X[:, t + 1], left_stim))[0]
            r_stim_trials = torch.where(torch.isin(X[:, t + 1], right_stim))[0]
            c_stim_trials = torch.where(torch.isin(X[:, t + 1], center_stim))[0]

            # For each trial, if center-stim transform latent into log probability
            # Outside stim trials are log(1)
            log_probs = model.temperature.exp() * z[c_stim_trials, 0]
            p = F.sigmoid(log_probs)
            cumulated_log_probs[c_stim_trials, t, 0] = p.log()
            cumulated_log_probs[c_stim_trials, t, 1] = (1 - p).log()

        # Flatten log probabilities
        cumulated_log_probs = cumulated_log_probs.view(-1, 2)
        y = y.view(-1)
        mask = mask.view(-1)
        X = X[:, 1:].reshape(-1)[mask == True]

        # Indices of different trial types
        l_stim_trials = torch.where(torch.isin(X, left_stim))[0]
        r_stim_trials = torch.where(torch.isin(X, right_stim))[0]
        c_stim_trials = torch.where(torch.isin(X, center_stim))[0]

        # Counts for different trial types
        total_count += mask.sum().item()
        outside_stim_count += len(l_stim_trials) + len(r_stim_trials)
        center_stim_count += len(c_stim_trials)

        # Calculate loss on legit trials
        loss = F.nll_loss(cumulated_log_probs, y.long(), reduction='none')
        masked_loss = loss * mask
        masked_loss[l_stim_trials] = 0
        masked_loss[r_stim_trials] = 0

        # Accumulate loss for different trial types
        total_loss += masked_loss.sum().item()
        outside_stim_loss += (masked_loss[l_stim_trials].sum() + masked_loss[r_stim_trials].sum()).item()
        center_stim_loss += masked_loss[c_stim_trials].sum().item()

        # Accumulate correct trials for computing accuracy
        probabilities = cumulated_log_probs[mask == True].exp()
        probabilities[l_stim_trials, 1] = 1
        probabilities[l_stim_trials, 0] = 0
        probabilities[r_stim_trials, 0] = 1
        probabilities[r_stim_trials, 1] = 0
        choices = probabilities.argmax(-1)
        choices = choices == y[mask == True]
        outside_stim_correct += torch.cat([choices[l_stim_trials], choices[r_stim_trials]]).sum()
        center_stim_correct += choices[c_stim_trials].sum()
        total_correct += choices.sum()
        probabilities = probabilities[torch.arange(len(probabilities)), y[mask == True].int()]
        probs.append(probabilities)
        outside_stim_probs.append(torch.cat([probabilities[l_stim_trials], probabilities[r_stim_trials]]))
        center_stim_probs.append(probabilities[c_stim_trials])

    summary['total_acc'].append(total_correct / total_count)
    summary['center_stim_acc'].append(center_stim_correct / center_stim_count)
    summary['outside_stim_acc'].append(outside_stim_correct / outside_stim_count)

    summary['total_loss'].append(total_loss / total_count)
    summary['center_stim_loss'].append(center_stim_loss / center_stim_count)
    summary['outside_stim_loss'].append(outside_stim_loss / outside_stim_count)

    probs = torch.cat(probs)
    outside_stim_probs = torch.cat(outside_stim_probs)
    center_stim_probs = torch.cat(center_stim_probs)
    summary['total_score'].append(probs.mean().item())
    summary['center_stim_score'].append(center_stim_probs.mean().item())
    summary['outside_stim_score'].append(outside_stim_probs.mean().item())

    return summary

def latent(model: LinearSwitching, dataset: LinearSwitchingDataset, session: int) -> np.ndarray:
    zs = []
    X, y = dataset[session]
    with torch.no_grad():
        T = len(X)
        z = model.z_0.unsqueeze(0)
        X = X.unsqueeze(0)
        for t in range(T - 1):
            zs.append(z)
            z = model(z, X[:, t])
    zs = torch.stack(zs).detach()
    return zs[:, 0, 0]