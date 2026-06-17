import time
from datetime import date
from pathlib import Path
from scrape_funcs import get_data, get_pie_feature


def make_year_directory(directory, year):
    '''Checks if the year input exists as a directory and creates it if not'''
    print(f'Checking for {year} directory presence......', end='')
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        print(f'New {year} directory created!')
    else:
        print('Already constructed!')


def save_data(directory, year):
    '''This function checks if the appropriate files exist yet within the year's folder, then generates/saves them if necessary'''
    
    generator_dict = {'plyr_per_game.csv': lambda: get_data(year, 'per_game').to_csv(f'{directory}/plyr_per_game.csv'),
                    'plyr_advanced.csv': lambda: get_data(year, 'advanced').to_csv(f'{directory}/plyr_advanced.csv'),
                    'mvp.csv': lambda: get_data(year, None, 'mvp').to_csv(f'{directory}/mvp.csv'),
                    'pie.csv': lambda: get_pie_feature(year).to_csv(f'{directory}/pie.csv'),
                    'adv_team_stats.csv': lambda: get_data(year, None, 'team').to_csv(f'{directory}/adv_team_stats.csv')
                    }
    
    existing_files = {file.name for file in directory.iterdir() if file.is_file()}
    expected_files = {'adv_team_stats.csv', 'plyr_per_game.csv', 'plyr_advanced.csv', 'mvp.csv', 'pie.csv'}
    missing_files = expected_files - existing_files

    for i in missing_files:
        print(f'Generating {year} {i}......', end='')

        for attempt in range(3):
            try:
                generator_dict[i]()

            except Exception as e:
                print(f'ATTEMPT #{attempt+1} FAILED: {e}.')
                time.sleep(10)

            else:
                print('Generation successful!')
                break

        time.sleep(3) #avoid overloading servers

    print(f'All files present for {year}.', end='\n\n')



if __name__ == '__main__':
    script_dir = Path(__file__).parent.resolve()
    repo_dir = script_dir.parent
    data_dir = Path(repo_dir/'data')

    year_list = list(range(1997, date.today().year + 1))

    for year in year_list:
        directory = data_dir/str(year)
        
        make_year_directory(directory, year)
        save_data(directory, year)