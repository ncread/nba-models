import sys
import time
from datetime import date
import pandas as pd
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.resolve())

from providers import get_bballref, get_nba
from helpers import make_directory, save_data, load_json, save_json
from transform import transform_all


script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
raw_dir = Path(repo_dir/'data'/'raw')
json_path = Path(repo_dir/'seasons.json')

SEASON_YEAR = (pd.Timestamp.now() + pd.DateOffset(months=3)).year 


def fetch_weekly(season_year) -> dict:
    json_file = load_json(json_path)
    current_day = str(date.today())     

    if json_file["seasons"][str(season_year)]["season_over"]:
        print(f'End of season stats already pulled for {season_year}. Exiting...')
        return

    season_api_string = json_file["seasons"][str(season_year)]["api_string"]

    year_dir = raw_dir/str(season_year)
    week_dir = year_dir/'weekly'/current_day

    make_directory(year_dir)
    make_directory(week_dir)


    print('Fetching 4 dataframes...')
    data = {'plyr_per_game': get_bballref(season_year, 'per_game')}
    time.sleep(2)

    data['plyr_advanced'] = get_bballref(season_year, 'advanced')
    time.sleep(2)

    data['adv_team_stats'] = get_bballref(season_year, None, 'team')

    data['pie'] = get_nba(season_api_string)

    print('Dataframe extractions successful')

    if current_day > json_file["seasons"][str(season_year)]["season_end"]:
        make_directory(year_dir/'final')
        save_data(data, year_dir/'final')
        json_file["seasons"][str(season_year)]["season_over"] = True
        print('Season set to finalized')
        save_json(json_file, json_path)
    else:
        save_data(data, week_dir)


if __name__ == '__main__':
    fetch_weekly(SEASON_YEAR)
    transform_all(SEASON_YEAR)