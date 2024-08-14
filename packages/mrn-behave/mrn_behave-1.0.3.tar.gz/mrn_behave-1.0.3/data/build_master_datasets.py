import os
from data_utils import build_master_datasets_for_subjects

def main():
    data_path = os.path.join(os.curdir, 'subjects')
    all_subjects = os.listdir(data_path)
    build_master_datasets_for_subjects(all_subjects)

if __name__ == '__main__':
    main()