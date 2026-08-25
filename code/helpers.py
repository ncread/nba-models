from pathlib import Path
import pandas as pd


def make_directory(directory: Path, new_folder: str):
    '''Within the given directory, checks if the new_folder string input exists as a directory and creates it if not'''
    print(f'Checking for {new_folder} directory presence...', end='')
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'New directory created!')
    else:
        print(f'Already constructed!')


def save_data(data_dict: dict[str:pd.DataFrame], directory: Path):
    '''Loops through a dictionary containing name:dataframe pairs and saves each dataframe as a csv file'''
    for name, df in data_dict.items():
        df.to_csv(directory/f'{name}.csv')