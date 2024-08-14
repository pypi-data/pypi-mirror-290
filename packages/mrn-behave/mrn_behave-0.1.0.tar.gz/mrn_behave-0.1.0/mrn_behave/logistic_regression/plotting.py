import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression


def plot_log_reg_coefs(model: LogisticRegression) -> None:
    labels = [
        r'$-80^\circ$, rewarded',
        r'$0^\circ$, rewarded, left-block',
        r'$0^\circ, rewarded, right-block',
        r'$+80^\circ$, rewarded, right-block',
        r'$-80^\circ$, no reward',
        r'$0^\circ$, no reward, left-block',
        r'$0^\circ$, no reward, right-block',
        r'$+80^\circ$, no reward'
    ]
    coefs = model.coef_.reshape(8, 10)
    lmda = 1 / model.get_params()['C']

    fig, ax = plt.subplots(2, 4, sharey=True, figsize=(12, 6))

    for i in range(4):
        ax[0, i].axhline(0, ls ='--', c='black', lw=0.7)
        ax[0, i].plot(coefs[i])
        ax[0, i].set_title(labels[i])
        


        ax[1, i].plot(coefs[i + 4])
        ax[1, i].axhline(0, ls ='--', c='black', lw=0.7)
        ax[1, i].set_title(labels[i + 4])
    
    fig.suptitle(rf'model coefficients, $\lambda = {lmda:0.4f}$')
    fig.tight_layout()
    plt.show()