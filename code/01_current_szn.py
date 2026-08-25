import time
from datetime import date
import pandas as pd
from pathlib import Path
from code.providers import get_bballref, get_nba
from code.helpers import make_directory, save_data

'''Runs weekly during the NBA season'''

def extract_weekly_data(year: int, current_season: str) -> dict:
    '''Sources the dataframes from bball ref and nba sites and populates a dictionary containing file names and the corresponding dataframes'''
    print('Extracting 4 dataframes...')
    data_dict = {'plyr_per_game': get_bballref(year, 'per_game')}
    time.sleep(2)

    data_dict['plyr_advanced'] = get_bballref(year, 'advanced')
    time.sleep(2)

    data_dict['adv_team_stats'] = get_bballref(year, None, 'team')
    time.sleep(2)

    data_dict['pie'] = get_nba(current_season)
    print('Dataframe extractions successful.')
    return data_dict


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