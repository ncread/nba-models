import time
from datetime import date
from pathlib import Path
from bball_ref import get_data


##########################################################################

#this file will be run once per day (~6 AM) to capture changes to the data from previous day's games

##########################################################################

#2025-26 season
# reg_season_end = '' #if we are more than 1 day beyond end of reg season, don't run. but once we hit beginning of next, year is year+1

#this allows us to both develop locally as well as save data appropriately within our gh workflow
script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent

current_year = date.today().year
current_date = date.today()


def make_directory(folder_name):
    # folder_path = Path(f'./data/{folder_name}')
    folder_path = repo_dir/'data'/str(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)


def save_data(year: int, date: str):
    '''
    Saves data for ongoing season
    Checks existence of year and date directories, and generates csv files for the current date
    '''

    # year_directory = Path(f'./data/{year}')
    # day_directory = Path(f'./data/{year}/{date}')
    year_directory = repo_dir/'data'/str(year)
    day_directory = repo_dir/'data'/str(year)/str(date)

    if not year_directory.is_dir():
        print(f'Creating directory for {year}')
        make_directory(year)
    if not day_directory.is_dir():
        print(f'Creating directory for {date}')
        # day_path = Path(day_directory)
        day_directory.mkdir(parents=True, exist_ok=True)
    

        team_dfs = get_data(year, None, 'team')

        generator_dict = {f'{date}_plyr_per_game.csv': lambda: get_data(year, 'per_game').to_csv(day_directory/'plyr_per_game.csv'),
                            f'{date}_plyr_advanced.csv': lambda: get_data(year, 'advanced').to_csv(day_directory/'plyr_advanced.csv'),
                            f'{date}_team_per_game.csv': lambda: team_dfs[0].to_csv(day_directory/'team_per_game.csv'),
                            f'{date}_opp_team_per_game.csv': lambda: team_dfs[1].to_csv(day_directory/'opp_team_per_game.csv'),
                            f'{date}_adv_team_stats.csv': lambda: team_dfs[2].to_csv(day_directory/'adv_team_stats.csv')
        }

        for i in generator_dict:
            print(f'Generating {i}')
            generator_dict[i]()
            time.sleep(3) #avoid overloading bref server
        print(f'All files present for {date}')
    else:
        print(f'{day_directory} directory is already present')


if __name__ == '__main__':
    save_data(current_year, current_date)