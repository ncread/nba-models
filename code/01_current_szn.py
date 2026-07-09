import time
from datetime import date
import pandas as pd
from pathlib import Path
from scrape_funcs import get_data, get_pie_feature

'''Runs weekly during the NBA season'''

def make_directory(directory: Path, timestamp: str):
    '''Checks if the date timestamp input exists as a directory and creates it if not'''
    print(f'Checking for {timestamp} directory presence......', end='')
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'New {timestamp} directory created!')
    else:
        print('Already constructed!')


def extract_weekly_data(year: int, current_season: str) -> dict:
    '''Sources the dataframes from bball ref and nba sites and populates a dictionary containing file names and the corresponding dataframes'''
    print('Extracting 4 dataframes...')
    data_dict = {'plyr_per_game': get_data(year, 'per_game')}
    time.sleep(2)

    data_dict['plyr_advanced'] = get_data(year, 'advanced')
    time.sleep(2)

    data_dict['adv_team_stats'] = get_data(year, None, 'team')
    time.sleep(2)

    data_dict['pie'] = get_pie_feature(current_season)
    print('Dataframe extractions successful.')
    return data_dict


def save_data(data_dict: dict[str: pd.DataFrame], week_dir: Path):
    '''Loops through the dictionary and saves each dataframe as a csv file'''
    for name, df in data_dict.items():
       df.to_csv(week_dir/f'{name}.csv') 


def main():
    script_dir = Path(__file__).parent.resolve()
    repo_dir = script_dir.parent
    data_dir = Path(repo_dir/'data')

    current_day = str(date.today())
    adjusted_year = (pd.Timestamp.now() + pd.DateOffset(months=3)).year
    current_season = str(adjusted_year - 1) + '-' + str(adjusted_year)[-2:]
    print(f'Current season is: {current_season}')

    year_dir = data_dir/str(adjusted_year)
    week_dir = data_dir/str(adjusted_year)/current_day


    make_directory(year_dir, str(adjusted_year))
    make_directory(week_dir, current_day)

    data = extract_weekly_data(adjusted_year, current_season)
    print('Success. Saving....', end='')
    save_data(data, week_dir)
    print('Success.')

if __name__ == '__main__':
    main()