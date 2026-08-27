import sys
from pathlib import Path
from datetime import date
from helpers import make_directory, save_data, load_json, save_json
from providers import get_bballref
sys.path.insert(0, Path(__file__).parent.resolve())


script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
data_dir = Path(repo_dir/'data')
json_path = Path(repo_dir/'seasons.json')


def fetch_mvp():
    current_year = date.today().year
    season_str = str(current_year)

    json_file = load_json(json_path)
    season_meta = json_file["seasons"].get(season_str)

    if not season_meta:
        print(f'No season entry found for {season_str}. Exiting...')
        return
    if season_meta["mvp_pulled"]:
        print(f'MVP standings already pulled for {season_str}. Exiting...')
        return

    df = get_bballref(current_year, None, 'mvp')

    make_directory(data_dir/season_str)
    save_data(df, data_dir/season_str/'mvp.csv')

    json_file["seasons"][season_str]["status"] = "finalized"
    json_file["seasons"][season_str]["mvp_pulled"] = True
    save_json(json_file, json_path)
    print(f'MVP results saved for {season_str} and season status set to finalized')


if __name__ == '__main__':
    fetch_mvp()