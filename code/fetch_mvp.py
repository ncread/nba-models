import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, Path(__file__).parent.resolve())

from helpers import save_data, load_json, save_json
from providers import get_bballref
from transform import transform_all

script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
raw_dir = Path(repo_dir/'data'/'raw')
json_path = Path(repo_dir/'seasons.json')

current_year = date.today().year

def fetch_mvp_func(year):
    season_str = str(year)

    json_file = load_json(json_path)
    season_meta = json_file["seasons"].get(season_str)

    if not season_meta:
        print(f'No season entry found for {season_str}. Exiting...')
        return

    mvp_path = raw_dir/'final'/'mvp.csv'
    if season_meta["mvp_pulled"] or mvp_path.is_file():
        json_file["seasons"][season_str]["mvp_pulled"] = True
        print(f'MVP standings already pulled for {season_str} or JSON field is mistakenly toggled. Exiting...')
        return

    df = get_bballref(year, None, 'mvp')

    final_path = raw_dir/season_str/'final'
    save_data(df, final_path/'mvp.csv')

    json_file["seasons"][season_str]["season_over"] = True
    json_file["seasons"][season_str]["mvp_pulled"] = True
    save_json(json_file, json_path)
    print(f'MVP results saved for {season_str} and season status set to finalized')


if __name__ == '__main__':
    fetch_mvp_func(current_year)
    transform_all(current_year)