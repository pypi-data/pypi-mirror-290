import numpy as np
import pickle
import os
import yaml
from torch.nn.utils.rnn import pad_sequence


def load_behavioral_data(subject: str) -> list[np.ndarray]:
    '''
    Helper function for loading behavioral data CSV file for a specific mouse
    and separating their data by sessions.
    '''

    csv_path = os.path.join(os.curdir, 'subjects', subject, f'{subject}behavioralData.csv')
    dataset = np.loadtxt(csv_path, delimiter=',')
    
    unique_sessions = np.unique(dataset[:, -1])
    split_by_session = [
        (session, dataset[dataset[:, -1] == session]) for session in unique_sessions
    ]
    return split_by_session


def filter_data(dataset: list[np.ndarray]) -> list[np.ndarray]:
    '''
    Filters down dataset. Each session must have greater than 200 trials, 60%
    or higher performance on the center stim trials for each block, and 80%
    or higher performance on the outside stim trials for each block.
    '''
    def check_outside_stim():
        l_block_outside_stim = outside_stim_trials[outside_stim_trials[:, 3] == -1]
        r_block_outside_stim = outside_stim_trials[outside_stim_trials[:, 3] == 1]

        l_block_correct = (l_block_outside_stim[:, 2] == 1).sum()
        r_block_correct = (r_block_outside_stim[:, 2] == 1).sum()

        if len(outside_stim_trials) == 0:
            return False
        return (l_block_correct / len(l_block_outside_stim)) > 0.8 and \
               (r_block_correct / len(r_block_outside_stim)) > 0.8
    
    def check_center_stim():
        l_block_center_stim = center_stim_trials[center_stim_trials[:, 3] == -1]
        r_block_center_stim = center_stim_trials[center_stim_trials[:, 3] == 1]
        if len(l_block_center_stim) == 0:
            return False
        elif len(r_block_center_stim) == 0:
            return False
        else:
            l_block_correct = (l_block_center_stim[:, 2] == 1).sum()
            r_block_correct = (r_block_center_stim[:, 2] == 1).sum()
        return (l_block_correct / len(l_block_center_stim)) > 0.6 and \
               (r_block_correct / len(r_block_center_stim)) > 0.6


    new_dataset = []

    for (session_id, data) in dataset:
        if len(data) < 200:
            continue
        outside_stim_trials = data[data[:, 0] != 0]
        center_stim_trials = data[data[:, 0] == 0]
        if check_outside_stim() and check_center_stim():
            new_dataset.append((session_id, data))
    return new_dataset



def organize_data(dataset: list) -> list:
    '''
    Takes a data list where each list is a np array of the behavioral data from a
    different session and organizes it into a dictionary that allows easy access
    of input/output pairs and other info about sessions.
    '''

    organized_dataset = []

    for (session_id, data) in dataset:
        organized_dataset.append(
            {
                'session_id' : session_id,
                'X' : data[:, :3],
                'y' : data[:, 1],
                'block_label' : data[:, 3]
            }
        )
    
    return organized_dataset


def save_master_dataset(subject: str, dataset: list) -> None:
    '''
    Builds master datasets for all subjects
    '''
    master_dataset_path = os.path.join(os.curdir, 'subjects', subject, 'master_dataset.pkl')
    with open(master_dataset_path, 'wb') as f:
        pickle.dump(dataset, f)
    print(f'Saved master dataset for subject {subject} at {master_dataset_path}')


def build_master_datasets_for_subjects(subjects: list[str]) -> None:
    for subject in subjects:
        behavioral_data = organize_data(filter_data(load_behavioral_data(subject)))
        save_master_dataset(subject, behavioral_data)

def load_master_dataset(subject: str) -> dict:
    path = os.path.join(
        os.curdir,
        'data',
        'subjects',
        subject,
        'master_dataset.pkl'
    )
    with open(path, 'rb') as file:
        dataset = pickle.load(file)
    
    return dataset



def make_tvt_split(dataset: list[dict], split_ratios: tuple=(0.7, 0.15, 0.15)):
    num_sessions = len(dataset)
    train_ratio, val_ratio, _ = split_ratios
    train_end = int(num_sessions * train_ratio)
    val_end = train_end + int(num_sessions * val_ratio)
    
    
    sessions = list(map(lambda x: int(x['session_id']), dataset))
    np.random.shuffle(sessions)
    train_sessions = sessions[:train_end]
    val_sessions = sessions[train_end:val_end]
    test_sessions = sessions[val_end:]

    split = {
        'train' : train_sessions,
        'val' : val_sessions,
        'test' : test_sessions
    }
    
    return split


def build_subject_splits(subjects: list[str]):

    path = os.path.join(
        os.curdir,
        'data',
        'subjects'
    )

    for subject in subjects:
        split_path = os.path.join(path, subject, 'splits')
        dataset = load_master_dataset(subject)
        for idx, split in enumerate(range(5)):
            split = make_tvt_split(dataset)
            print(split)
            split_file = os.path.join(split_path, f'split_{idx + 1}.yaml')
            with open(split_file, 'w') as f:
                yaml.dump(split, f)


def load_split(subject: str, fold: int) -> dict:
    path = os.path.join(
        os.curdir,
        'data',
        'subjects',
        subject,
        'splits',
        f'split_{fold}.yaml'
    )
    with open(path, 'r') as f:
        session_split = yaml.safe_load(f)
    return session_split

def custom_collate_fn(batch):
    X, y = zip(*batch)
    
    padded_X = pad_sequence(X, batch_first=True, padding_value=-999)
    padded_y = pad_sequence(y, batch_first=True, padding_value=-999)
    mask = (padded_y != -999)
    padded_X[padded_X == -999] = 0
    padded_y[padded_y == -999] = 0
    return padded_X, padded_y, mask