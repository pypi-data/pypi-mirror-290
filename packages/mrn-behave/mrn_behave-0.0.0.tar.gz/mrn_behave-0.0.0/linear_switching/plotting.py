import torch
import numpy as np
import matplotlib.pyplot as plt
from linear_switching.linear_switching import LinearSwitching
plt.style.use('ggplot')

def train_summary(summary: dict, save: str=None) -> None:

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    colors = {'train' : 'C0', 'val' : 'C1'}
    linestyles = {'total' : 'solid', 'center' : 'dashed', 'outside' : 'dashdot'}

    for split in summary.keys():
        if split == 'model':
            continue
        for idx, metric in enumerate(summary[split].keys()):
            metric_words = metric.split('_')
            if 'loss' in metric_words:
                ax[0].plot(summary[split][metric], c=colors[split], ls=linestyles[metric_words[0]], label=metric_words[0])
            elif 'score' in metric_words:
                ax[1].plot(summary[split][metric], c=colors[split], ls=linestyles[metric_words[0]], label=metric_words[0])
            else:
                ax[2].plot(summary[split][metric], c=colors[split], ls=linestyles[metric_words[0]], label=metric_words[0])
    
    ax[0].set_title('loss')
    ax[0].set_ylabel('avg. NLL')
    ax[0].set_xlabel('epochs')
    ax[1].set_title('score')
    ax[1].set_ylabel(r'avg. $P(y\mid x, \theta)$')
    ax[1].set_xlabel('epochs')
    ax[2].set_title('accuracy')
    ax[2].set_xlabel('epochs')
    ax[2].set_ylabel('fraction correct')

    fig.legend(['train total', 'train center', 'train outside', 'val total', 'val center', 'val outside'], bbox_to_anchor=(1.1, 1))
    fig.suptitle('performance across training')
    fig.tight_layout()
    
    if save is not None:
        plt.savefig(save)


def plot_update_rules(model: LinearSwitching, z_min: float, z_max: float, save: str=None) -> None:

    labels = [
        's=-80, a=+1, r=1',
        's=0, a=-1, r=1',
        's=0, a=1, r=1',
        's=+80, a=-1, r=1',
        's=-80, a=-1, r=0',
        's=0, a=1, r=0',
        's=0, a=-1, r=0',
        's=+80, a=1, r=0'
    ]

    coefficients = model.coefs
    offsets = model.offsets
    x_range = np.linspace(z_min, z_max, 1000)
    fig, ax = plt.subplots(2, 4, figsize=(15, 10))



    for i in range(4):

        # First row
        ax[0, i].plot(x_range, coefficients[i] * x_range + offsets[i])
        ax[0, i].set_xlabel('$z_t$')
        ax[0, i].set_ylabel('$z_{t+1}$')
        ax[0, i].set_title(labels[i])
        ax[0, i].axvline(0, ls='--', c='black', lw=0.5)
        ax[0, i].axhline(0, ls='--', c='black', lw=0.5)
        ax[0, i].set_box_aspect(1)
        ax[0, i].set_xlim(z_min, z_max)
        ax[0, i].set_ylim(z_min, z_max)
        ax[0, i].plot(np.linspace(z_min, z_max), np.linspace(z_min, z_max), c='black', ls='--')

        # Second row
        ax[1, i].plot(x_range, coefficients[i + 4] * x_range + offsets[i + 4])
        ax[1, i].set_xlabel('$z_t$')
        ax[1, i].set_ylabel('$z_{t+1}$')
        ax[1, i].set_title(labels[i + 4])
        ax[1, i].axvline(0, ls='--', c='black', lw=0.5)
        ax[1, i].axhline(0, ls='--', c='black', lw=0.5)
        ax[1, i].set_box_aspect(1)
        ax[1, i].set_xlim(z_min, z_max)
        ax[1, i].set_ylim(z_min, z_max)
        ax[1, i].plot(np.linspace(z_min, z_max), np.linspace(z_min, z_max), c='black', ls='--')
    fig.tight_layout()
    if save is not None:
        plt.savefig(save)

