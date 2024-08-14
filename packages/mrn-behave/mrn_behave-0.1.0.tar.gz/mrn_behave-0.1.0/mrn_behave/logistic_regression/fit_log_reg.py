import numpy as np
from sklearn.linear_model import LogisticRegression
from ..logistic_regression.log_reg_utils import LogisticRegressionDataset
from sklearn.metrics import accuracy_score

def train(subject: str, fold: int, penalty_type: str | None = None, lmda: float=0) -> dict:

    def _compute_score(X: np.ndarray, y: np.ndarray) -> float:
        y[y == -1] = 0
        all_probs = model.predict_proba(X)
        p_y_given_x = all_probs[np.arange(len(y)), y.astype(int)]
        return p_y_given_x.mean()


    summary = {
        split : {
            'score' : None,
            'acc' : None
        } for split in ['train', 'val']
    }
    
    train_set = LogisticRegressionDataset(subject, 'train', fold)
    val_set = LogisticRegressionDataset(subject, 'val', fold)

    X_train, y_train = train_set.build_dataset()
    X_val, y_val = val_set.build_dataset()

    if penalty_type is not None:

        model = LogisticRegression(penalty=penalty_type, C = 1 / lmda, solver='liblinear')
    
    else:
        model = LogisticRegression(solver='liblinear')

    model.fit(X_train, y_train)

    summary['train']['score'] = _compute_score(X_train, y_train)
    summary['train']['acc'] = accuracy_score(y_train, model.predict(X_train))

    summary['val']['score'] = _compute_score(X_val, y_val)
    summary['val']['acc'] = accuracy_score(y_val, model.predict(X_val))

    summary['model'] = model

    return summary
