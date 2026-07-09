'''This script is somewhat similar to 01_current_szn.py, yet it is intended to be executed following MVP results being released, thus it is scheduled to run on July 1st each year.It will also save all of the files in the raw year directory, not within a weekly subfolder. The presence of these files denotes that the corresponding regular season is over and MVP results have been extracted and saved.'''

import time
from datetime import date
import pandas as pd
from pathlib import Path
from scrape_funcs import get_data, get_pie_feature


def make_directory(directory: Path, year: int):
    '''Checks if the year input exists as a directory and creates it if not'''
    print(f'Checking for {year} directory......', end='')
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'New {year} directory created!')
    else:
        print('Already constructed! ', end='')


def extract_past_data(year: int, current_season: str, year_dir: Path) -> dict:
    existing_files = {file.name for file in year_dir.iterdir() if file.is_file()}
    expected_files = {'plyr_per_game.csv', 'plyr_advanced.csv', 'adv_team_stats.csv', 'pie.csv', 'mvp.csv'}
    missing_files = expected_files - existing_files

    data_dict = {}
    if len(missing_files) > 0:
        print(f'Extracting {missing_files} for {year}...', end='')

        if 'plyr_per_game.csv' in missing_files:
            data_dict = {'plyr_per_game': get_data(year, 'per_game')}
            time.sleep(2)
        if 'plyr_advanced.csv' in missing_files:
            data_dict['plyr_advanced'] = get_data(year, 'advanced')
            time.sleep(2)
        if 'adv_team_stats.csv' in missing_files:
            data_dict['adv_team_stats'] = get_data(year, None, 'team')
            time.sleep(2)
        if 'pie.csv' in missing_files:
            data_dict['pie'] = get_pie_feature(current_season) 
            time.sleep(2)
        if 'mvp.csv' in missing_files:
            data_dict['mvp'] = get_data(year, None, 'mvp')

        print('Dataframe extractions successful.')
    else:
        print('All files present.')
    return data_dict


def save_past_data(data_dict: dict[str: pd.DataFrame], year_dir: Path):
    for name, df in data_dict.items():
        df.to_csv(year_dir/f'{name}.csv')


def main():
    script_dir = Path(__file__).parent.resolve()
    repo_dir = script_dir.parent
    data_dir = Path(repo_dir/'data')

    adjusted_year = (pd.Timestamp.now() + pd.DateOffset(months=3)).year

    year_list = list(range(1997, date.today().year + 1))
    for year in year_list:
        current_season = str(year - 1) + '-' + str(year)[-2:]
        # print(f'Loop iter: {year}. Most recent season: {current_season}')

        year_dir = data_dir/str(year)

        make_directory(year_dir, str(year))

        #maybe add logic checking for file existence down the line
        data = extract_past_data(year, current_season, year_dir)

        save_past_data(data, year_dir)

if __name__ == '__main__':
    main()