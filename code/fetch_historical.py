import sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.resolve())

from helpers import make_directory, save_data, load_json
from providers import get_bballref, get_nba
from fetch_mvp import fetch_mvp_func
from transform import transform_all


script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
train_dir = Path(repo_dir/'data'/'train')
raw_dir = Path(repo_dir/'data'/'raw')
json_file = load_json(repo_dir/'seasons.json')

current_year = datetime.now().year

EXPECTED_FILES = {'plyr_per_game.csv','plyr_advanced.csv','adv_team_stats.csv','pie.csv','mvp.csv'}


def check_missing_files(year_dir):
    present_files = {f.name for f in year_dir.iterdir() if f.is_file()}
    missing = EXPECTED_FILES - present_files
    return missing


def fetch_historical():
    for year_dir in raw_dir.iterdir():
        try:
            season_year = int(year_dir.name)
        except ValueError:
            print(f'{year_dir} is not a year. Skipping...')
            continue

        print('-----------------------------------------------')
        print(f'{season_year}')

        if not year_dir.is_dir() or not json_file["seasons"][str(season_year)]["season_over"]:
            print(f'{season_year} season not over! Skipping...')
            continue

        print(f'Checking files in {season_year}/...', end='')

        final_path = year_dir/'final'
        missing = check_missing_files(final_path)
        if not missing:
            print(f'All raw files present for {season_year}')

        else:
            print(f'Missing {missing} for {season_year}. Fetching...')
        
            season_api_string = json_file["seasons"][str(year_dir.name)]["api_string"]

            fetch_map = {'plyr_per_game.csv': lambda path: save_data(get_bballref(season_year, 'per_game'), path/'plyr_per_game.csv'),
                        'plyr_advanced.csv': lambda path: save_data(get_bballref(season_year, 'advanced'), path/'plyr_advanced.csv'),
                        'adv_team_stats.csv': lambda path: save_data(get_bballref(season_year, None, 'team'), path/'adv_team_stats.csv'),
                        'pie.csv': lambda path: save_data(get_nba(season_api_string), path/'pie.csv'),
                        'mvp.csv': lambda path: fetch_mvp_func(season_year)}
            try:
                for file in missing:
                    fetch_map[file](final_path)
            except:
                print(f'Issue trying to fetch {missing} for {season_year}. Skipping transformation and further fetching...')
                continue

        train_path = train_dir/f'{season_year}.parquet'
        if train_path.is_file():
            print(f'Transformed file for {season_year} already exists. Skipping...')
            continue
        
        else:
            print('No train file present. Transforming files...')
            transform_all(season_year)
            print(f'Files transformed and {season_year}.parquet created and saved!')


if __name__ == '__main__':
    fetch_historical()