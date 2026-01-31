import time
import pandas as pd
from datetime import date
from pathlib import Path

##########################################################################

#we want to run this data-generating script once each season is completed, 
#so in the summer (~July 1st) the previous season's full data will be added to the training data

##########################################################################

year_list = list(range(1975, date.today().year + 1)) #to include this year's data (runs on 07/01)
# year_list = list(range(1975, date.today().year)) #generates all dataframes
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

def get_data(year: int, table_type: str, trigger = None) -> pd.DataFrame:
    if trigger == 'mvp':
        url = f'https://www.basketball-reference.com/awards/awards_{year}.html#all_mvp'

    elif trigger == 'team':
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'

        tables = pd.read_html(url, storage_options=headers)
        time.sleep(3)
        if year > 2015: #basketball reference began including conference standings in 2016, altering webpage structure
            team_per_game = tables[4]
            opp_per_game = tables[5]
            adv_team_stats = tables[10]
        else:
            team_per_game = tables[2]
            opp_per_game = tables[3]
            adv_team_stats = tables[8]

        return (team_per_game, opp_per_game, adv_team_stats)
    else:
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_{table_type}.html'


    tables = pd.read_html(url, storage_options=headers)
    time.sleep(3)
    df = tables[0]
    return df


def make_directory(folder_name):
    folder_path = Path(f'./data/{folder_name}')
    folder_path.mkdir(parents=True, exist_ok=True)


def save_data(year_list: list):
    '''
    Checks existence of year directory, and generates any csv files that it may be missing.
    '''

    for year in year_list:

        directory = Path(f'./data/{year}')
        if not directory.is_dir():
            print(f'Creating directory for {year}')
            make_directory(year)

        generator_dict = {'plyr_per_game.csv': lambda: get_data(year, 'per_game').to_csv(f'./data/{year}/plyr_per_game.csv'),
                          'plyr_advanced.csv': lambda: get_data(year, 'advanced').to_csv(f'./data/{year}/plyr_advanced.csv'),
                          'mvp.csv': lambda: get_data(year, None, 'mvp').to_csv(f'./data/{year}/mvp.csv')
        }

        #check for missing files
        existing_files = {file.name for file in directory.iterdir() if file.is_file()}
        all_files = {'team_per_game.csv', 'opp_team_per_game.csv', 'adv_team_stats.csv', 'plyr_per_game.csv', 'plyr_advanced.csv', 'mvp.csv'}
        missing_files = all_files - existing_files

        if 'team_per_game.csv' in missing_files:
            team_dfs = get_data(year, None, 'team')
            generator_dict['team_per_game.csv'] = lambda: team_dfs[0].to_csv(f'./data/{year}/team_per_game.csv')
            generator_dict['opp_team_per_game.csv'] = lambda: team_dfs[1].to_csv(f'./data/{year}/opp_team_per_game.csv')
            generator_dict['adv_team_stats.csv'] = lambda: team_dfs[2].to_csv(f'./data/{year}/adv_team_stats.csv')

        for i in missing_files:
            print(f'Generating {year} {i}')
            generator_dict[i]()
            time.sleep(3) #avoid overloading bref server
        print(f'All files present for {year}', end='\n\n')


if __name__ == '__main__':
    save_data(year_list)