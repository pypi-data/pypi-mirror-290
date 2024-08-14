from disrnn.disrnn import DisRNN
from disrnn.disrnn_utils import DisRNNDataset
from data.data_utils import custom_collate_fn
import torch
from torch import Tensor
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader



def train(
        subject: str,
        fold: int,
        epochs: int,
        lr: float,
        beta_weight: float
) -> None:
    
    # Setup
    model = DisRNN(
        num_latents=5,
        num_obs=3,
        include_stimulus=True,
        update_mlp_hidden_size=[5, 5, 5],
        choice_mlp_hidden_size=[3, 3]
    )
    model = torch.compile(model)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    train_set = DisRNNDataset(subject, 'train', fold)
    val_set = DisRNNDataset(subject, 'val', fold)
    train_loader = DataLoader(
        train_set,
        batch_size=8,
        collate_fn=custom_collate_fn
    )
    val_loader = DataLoader(
        val_set,
        batch_size=8,
        collate_fn=custom_collate_fn
    )

    summary = {
        split : {
            'loss': {
                'nll' : {
                    'total' : [],
                    'c_stim' : [],
                    'o_stim' : []
                },
                'kld' : {
                    'total' : [],
                    'c_stim' : [],
                    'o_stim' : []
                }
            },
            'score' : {
                'total' : [],
                'c_stim' : [],
                'o_stim' : []
            },
            'acc' : {
                'total' : [],
                'c_stim' : [],
                'o_stim' : []
            }

        }
        for split in ['train', 'val']
    }

    summary['model'] = {
        'global_sigmas' : [],
        'global_multipliers' : [],
        'update_sigmas' : [],
        'update_multipliers' : []
    }

    summary['grad_norm'] = []
    model_checkpoint = None


    # Begin training
    for epoch in range(epochs):
        for split in ['train', 'val']:
            if split == 'val':
                torch.set_grad_enabled(False)
                model.eval()
                loader = val_loader
                dataset = val_set
            else:
                torch.set_grad_enabled(True)
                model.train()
                loader = train_loader
                dataset = train_set
            
            epoch_c_stim_nll = 0
            epoch_o_stim_nll = 0

            epoch_c_stim_kld = 0
            epoch_o_stim_kld = 0

            epoch_c_stim_score = 0
            epoch_o_stim_score = 0
            
            epoch_c_stim_correct = 0
            epoch_o_stim_correct = 0


            for (X, y, mask) in loader:
                X = X.float()
                y = y.long()
                optimizer.zero_grad()
                if split == 'train':
                    summary['model']['global_sigmas'].append(model.global_sigmas)
                    summary['model']['global_multipliers'].append(model.global_multipliers)
                    summary['model']['update_sigmas'].append(model.update_sigmas)
                    summary['model']['update_multipliers'].append(model.update_multipliers)

                B, T, _ = X.shape

                # Initialize containers for loss
                cumulated_logits = torch.zeros(size=(B, T - 1, 2))
                cumulated_kld_loss = torch.zeros(size=(B, T - 1))

                # Iterate over timesteps
                # Forward pass
                for t in range(T - 1):
                    obs = X[:, t]
                    s_t = X[:, t + 1, 0].unsqueeze(-1)
                    if t == 0:
                        dummy_z0 = torch.zeros(size=(B, model.num_latents))
                        logits, updated_z, global_kld, update_kld = model.forward(
                            dummy_z0, obs, True, s_t
                        )
                    else:
                        logits, updated_z, global_kld, update_kld = model.forward(
                            updated_z, obs, False, s_t
                        )

                    cumulated_logits[:, t] = logits
                    global_kld = global_kld.sum()
                    update_kld = update_kld.sum()
                    cumulated_kld_loss[:, t] = global_kld + update_kld

                # Flatten and apply mask
                X = X[:, 1:, :].reshape(-1, 3)
                y = y.view(-1)
                cumulated_logits = cumulated_logits.view(-1, 2)
                kld_loss = cumulated_kld_loss.view(-1)
                mask = mask.view(-1)

                # Calculate cross entropy and apply mask to loss
                probs = cumulated_logits.softmax(-1)
                log_probs = probs.log()
                nll = F.nll_loss(log_probs, y, reduction='none')
                nll[mask == False] = 0
                kld_loss[mask == False] = 0

                # Backward pass
                loss = (nll + kld_loss * beta_weight).mean()
                print(split)
                if split == 'train':
                    loss.backward()
                    optimizer.step()

                # Get trial identity indices
                center_stim_trials = torch.where((X[:, 0] == 0) & (mask == True))
                outside_stim_trials = torch.where((X[:, 0] != 0) & (mask == True))

                # Filter loss by trial type
                epoch_c_stim_nll += nll[center_stim_trials].sum().item()
                epoch_o_stim_nll += nll[outside_stim_trials].sum().item()
                epoch_c_stim_kld += kld_loss[center_stim_trials].sum().item() * beta_weight
                epoch_o_stim_kld += kld_loss[outside_stim_trials].sum().item() * beta_weight

                # Compute score
                correct_probs = probs[torch.arange(len(probs)), y]
                epoch_c_stim_score += correct_probs[center_stim_trials].sum().item()
                epoch_o_stim_score += correct_probs[outside_stim_trials].sum().item()

                # Compute correct trials
                choice = probs.argmax(-1)
                correct_choices = (choice == y)
                epoch_c_stim_correct += correct_choices[center_stim_trials].sum()
                epoch_o_stim_correct += correct_choices[outside_stim_trials].sum()

            

            summary[split]['loss']['nll']['total'].append((epoch_c_stim_nll + epoch_o_stim_nll) / dataset.length)
            summary[split]['loss']['nll']['c_stim'].append(epoch_c_stim_nll / dataset.c_stim_trials)
            summary[split]['loss']['nll']['o_stim'].append(epoch_o_stim_nll / dataset.o_stim_trials)

            summary[split]['loss']['kld']['total'].append((epoch_c_stim_kld + epoch_o_stim_kld) / dataset.length)
            summary[split]['loss']['kld']['c_stim'].append(epoch_c_stim_kld / dataset.c_stim_trials)
            summary[split]['loss']['kld']['o_stim'].append(epoch_o_stim_kld / dataset.o_stim_trials)

            summary[split]['score']['total'].append((epoch_c_stim_score + epoch_o_stim_score) / dataset.length)
            summary[split]['score']['c_stim'].append(epoch_c_stim_score / dataset.c_stim_trials)
            summary[split]['score']['o_stim'].append(epoch_o_stim_score / dataset.o_stim_trials)

            summary[split]['acc']['total'].append((epoch_c_stim_correct + epoch_o_stim_correct) / dataset.length)
            summary[split]['acc']['c_stim'].append(epoch_c_stim_correct / dataset.c_stim_trials)
            summary[split]['acc']['o_stim'].append(epoch_o_stim_correct / dataset.o_stim_trials)

        print('=' * 30)
        print(f'Epoch {epoch + 1}')
        print('Training')
        print(f"NLL: {summary['train']['loss']['nll']['total'][-1]:0.4f}, KLD: {summary['train']['loss']['kld']['total'][-1]:0.4f}")
        print(f"Score: {summary['train']['score']['total'][-1]:0.4f}, Accuracy: {summary['train']['acc']['total'][-1]}")
        print('-' * 15)
        print('Validation')
        print(f"NLL: {summary['val']['loss']['nll']['total'][-1]:0.4f}, KLD: {summary['val']['loss']['kld']['total'][-1]:0.4f}")
        print(f"Score: {summary['val']['score']['total'][-1]:0.4f}, Accuracy: {summary['val']['acc']['total'][-1]}")
    return summary























