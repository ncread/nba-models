import json
import pandas as pd
from pathlib import Path


def make_directory(directory: Path) -> None:
    '''Within the given directory, checks if the new_folder string input exists as a directory and creates it if not'''
    print(f'Checking for {directory.as_posix()} presence...', end='')
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'New directory created!')
    else:
        print(f'Already constructed!')


def save_data(data: pd.DataFrame | dict[str:pd.DataFrame], directory: Path) -> None:
    '''Loops through a dictionary containing name:dataframe pairs and saves each dataframe as a csv file'''
    if isinstance(data, dict):
        for name, df in data.items():
            df.to_csv(directory/f'{name}.csv')
        print('Multiple dataframes successfully saved.')
    elif isinstance(data, pd.DataFrame):
        data.to_csv(directory)
        print(f'Dataframe successfully saved to {directory.as_posix()}')
    else:
        print('Input data is neither a dictionary nor a single dataframe')


def load_json(json_path: Path):
    with open(json_path) as f:
        return json.load(f)
    print(f'Loaded {json_path.as_posix()}')


def save_json(file, json_path: Path):
    with open(json_path, 'w') as f:
        json.dump(file, f, indent=2)
    print(f'Saved {json_path.as_posix()}')