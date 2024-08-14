import sys
sys.path.append('/Users/jeremyschroeter/Desktop/School_Work/Steinmetz_Lab/behavioral_modeling_2')
import torch
import torch.nn.functional as F
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from linear_switching.linear_switching import LinearSwitching
from linear_switching.linear_switching_utils import LinearSwitchingDataset
from data.data_utils import custom_collate_fn


def train(
        subject: str,
        fold: int,
        epochs: int,
        lr: float
) -> dict:
    

    model = LinearSwitching()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    train_set = LinearSwitchingDataset(subject, 'train', fold)
    val_set = LinearSwitchingDataset(subject, 'val', fold)
    
    train_loader = DataLoader(train_set, 8, collate_fn=custom_collate_fn)
    val_loader = DataLoader(val_set, 8, collate_fn=custom_collate_fn)
    stopping_criteria = 1e-4





    summary = {
        split : {
            'total_loss' : [],
            'center_stim_loss' : [],
            'outside_stim_loss' : [],
            'total_score' : [],
            'center_stim_score' : [],
            'outside_stim_score' : [],
            'total_acc' : [],
            'center_stim_acc' : [],
            'outside_stim_acc' : []
        } for split in [
            'train',
            'val'
        ]
    }

    summary['model'] = {'coefficients' : [], 'offsets' : []}


    # Data observation mapping
    left_stim = torch.tensor([0, 4])
    center_stim = torch.tensor([1, 2, 5, 6])
    right_stim = torch.tensor([3, 7])

    # Iterate over epochs
    for epoch in range(epochs):

        for split in ['train', 'val']:
            if split == 'val':
                torch.set_grad_enabled(False)
                model.eval()
                loader = val_loader
            else:
                torch.set_grad_enabled(True)
                model.train()
                loader = train_loader

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
                if split == 'train':
                    summary['model']['coefficients'].append(model.coefs)
                    summary['model']['offsets'].append(model.offsets)
                y[y == -1] = 0

                B, T = X.shape
                optimizer.zero_grad()
                cumulated_log_probs = torch.zeros(size=(B, T - 1, 2))
                z = model.z_0.expand(size=(B, 1))

                for t in range(T - 1):
                    z = model(z, X[:, t])
                    l_stim_trials = torch.where(torch.isin(X[:, t + 1], left_stim))[0]
                    r_stim_trials = torch.where(torch.isin(X[:, t + 1], right_stim))[0]
                    c_stim_trials = torch.where(torch.isin(X[:, t + 1], center_stim))[0]

                    log_probs = (1 / model.inv_temp.exp()) * z[c_stim_trials, 0]
                    p = torch.sigmoid(log_probs)
                    cumulated_log_probs[c_stim_trials, t, 0] = p.log()
                    cumulated_log_probs[c_stim_trials, t, 1] = (1 - p).log()

                cumulated_log_probs = cumulated_log_probs.view(-1, 2)
                y = y.view(-1)
                mask = mask.view(-1)
                X = X[:, 1:].reshape(-1)[mask]

                l_stim_trials = torch.where(torch.isin(X, left_stim))[0]
                r_stim_trials = torch.where(torch.isin(X, right_stim))[0]
                c_stim_trials = torch.where(torch.isin(X, center_stim))[0]

                total_count += mask.sum().item()
                outside_stim_count += len(l_stim_trials) + len(r_stim_trials)
                center_stim_count += len(c_stim_trials)

                loss = F.nll_loss(cumulated_log_probs, y.long(), reduction='none')
                masked_loss = loss * mask
                masked_loss[l_stim_trials] = 0
                masked_loss[r_stim_trials] = 0

                total_loss += masked_loss.sum().item()
                outside_stim_loss += (masked_loss[l_stim_trials].sum() + masked_loss[r_stim_trials].sum()).item()
                center_stim_loss += masked_loss[c_stim_trials].sum().item()

                if split == 'train':
                    masked_loss.mean().backward()
                    optimizer.step()

                probabilities = cumulated_log_probs[mask].exp()
                probabilities[l_stim_trials, 1] = 1
                probabilities[l_stim_trials, 0] = 0
                probabilities[r_stim_trials, 0] = 1
                probabilities[r_stim_trials, 1] = 0

                choices = probabilities.argmax(-1) == y[mask]
                outside_stim_correct += torch.cat([choices[l_stim_trials], choices[r_stim_trials]]).sum().item()
                center_stim_correct += choices[c_stim_trials].sum().item()
                total_correct += choices.sum().item()

                probabilities = probabilities[torch.arange(len(probabilities)), y[mask].long()]
                probs.append(probabilities)
                outside_stim_probs.append(torch.cat([probabilities[l_stim_trials], probabilities[r_stim_trials]]))
                center_stim_probs.append(probabilities[c_stim_trials])

            summary[split]['total_acc'].append(total_correct / total_count)
            summary[split]['center_stim_acc'].append(center_stim_correct / center_stim_count)
            summary[split]['outside_stim_acc'].append(outside_stim_correct / outside_stim_count)
            summary[split]['total_loss'].append(total_loss / total_count)
            summary[split]['center_stim_loss'].append(center_stim_loss / center_stim_count)
            summary[split]['outside_stim_loss'].append(outside_stim_loss / outside_stim_count)

            probs = torch.cat(probs)
            outside_stim_probs = torch.cat(outside_stim_probs)
            center_stim_probs = torch.cat(center_stim_probs)

            summary[split]['total_score'].append(probs.mean().item())
            summary[split]['center_stim_score'].append(center_stim_probs.mean().item())
            summary[split]['outside_stim_score'].append(outside_stim_probs.mean().item())

        print(f'Epoch {epoch + 1}')
        print(f"Training loss: {summary['train']['total_loss'][-1]:0.4f}, Training score: {summary['train']['total_score'][-1]:0.4f}, Training acc: {summary['train']['total_acc'][-1]:0.4f}")
        print(f"Validation loss: {summary['val']['total_loss'][-1]:0.4f}, Validation score: {summary['val']['total_score'][-1]:0.4f}, Validation acc: {summary['val']['total_acc'][-1]:0.4f}")

        if epoch > 1 and abs(summary['val']['total_loss'][-1] - summary['val']['total_loss'][-2]) < stopping_criteria:
            summary['model']['model'] = model
            return summary
    summary['model']['model'] = model
    return summary
