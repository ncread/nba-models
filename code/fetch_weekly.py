import sys
import time
from datetime import date
import pandas as pd
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.resolve())

from providers import get_bballref, get_nba
from helpers import make_directory, save_data, load_json, save_json


script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
data_dir = Path(repo_dir/'data')
json_path = Path(repo_dir/'seasons.json')


def fetch_weekly_data(year: int, current_season: str) -> dict:
    print('Fetching 4 dataframes...')
    data_dict = {'plyr_per_game': get_bballref(year, 'per_game')}
    time.sleep(2)

    data_dict['plyr_advanced'] = get_bballref(year, 'advanced')
    time.sleep(2)

    data_dict['adv_team_stats'] = get_bballref(year, None, 'team')

    data_dict['pie'] = get_nba(current_season)

    print('Dataframe extractions successful')

    return data_dict


if __name__ == '__main__':
    json_file = load_json(json_path)
    current_day = str(date.today())
    season_year = (pd.Timestamp.now() + pd.DateOffset(months=3)).year      

    if json_file["seasons"][str(season_year)]["status"] == "finalized":
        print(f'End of season stats already pulled for {season_year}. Exiting...')

    else:
        year_dir = data_dir/str(season_year)
        week_dir = year_dir/current_day

        make_directory(year_dir)
        make_directory(week_dir)

        season_api_string = json_file["seasons"][str(season_year)]["api_string"]   
        data = fetch_weekly_data(season_year, season_api_string)

        if current_day > json_file["seasons"][str(season_year)]["season_end"]:
            make_directory(year_dir/'final')
            save_data(data, year_dir/'final')
            json_file["seasons"][str(season_year)]["status"] = "finalized"
            print('Season set to finalized')
            save_json(json_file, json_path)

        save_data(data, week_dir)