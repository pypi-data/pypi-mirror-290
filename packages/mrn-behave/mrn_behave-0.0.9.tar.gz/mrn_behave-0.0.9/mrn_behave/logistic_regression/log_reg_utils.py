import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from ..data.data_utils import load_master_dataset, load_split


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
        # One_hot_encode
        one_hot_encoded = np.array(list(map(lambda x: observations[tuple(x)], session['X'])))
        
        one_hot_matrix = np.zeros(shape=(len(X), 8))
        one_hot_matrix[np.arange(len(X)), one_hot_encoded] = 1
        sliding = sliding_window_view(one_hot_matrix, 10, 0)
        session['X'] = sliding[:-1]
        session['y'] = session['y'][10:]
    return dataset


class LogisticRegressionDataset:
    def __init__(
            self,
            subject: str,
            split: str,
            fold: int
    ) -> None:
        
        full_dataset = load_master_dataset(subject)

        self.sessions = load_split(subject, fold)[split]
        self.dataset = list(filter(lambda x: x['session_id'] in self.sessions, full_dataset))
        self.center_stim_trials = list(map(lambda session: np.where(session['X'][10:, 0] == 0), self.dataset))
        self.outside_stim_trials = list(map(lambda session: np.where(session['X'][10:, 0] != 0), self.dataset))
        self.dataset = convert_dataset(self.dataset)
    
    
    def build_dataset(self) -> tuple[np.ndarray, np.ndarray]:

        X = [self.dataset[session]['X'][self.center_stim_trials[session]] for session in range(len(self.dataset))]
        X = np.vstack(X).reshape(-1, 80)
        y = [self.dataset[session]['y'][self.center_stim_trials[session]] for session in range(len(self.dataset))]
        y = np.hstack(y)
        return X, y


    def get_session(self, session_id: int) -> dict:
        
        for session in self.dataset:
            if session['session_id'] == session_id:
                return session
        raise KeyError('invalid session ID for this dataset')
    
