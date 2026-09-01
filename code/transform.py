import sys
import numpy as np
import pandas as pd
from datetime import date
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.resolve())

from helpers import make_directory, load_json

#want to run this every time fetch_weekly is run and every time fetch_mvp is run

#want to loop through the year dirs and check for "transformed.csv" or whatever it will be called. if present, continue through the loop. If absent, check for the expected 5 files (4 + mvp file), and perform transformations if they're all present. If something is missing, call a function from fetch_historical to fetch it.
#transform the raw data and save output to processed folder within data folder
    #raw data comes from output from either the July mvp script, to transform the end of season stats as a training dataset (or just add the rows to an existing training set in the directory somewhere), OR the weekly script, where data is brought together into one df. Predictions are then made on this data based on the trained model from the previous season.
# feature_trans takes in the year directory and outputs a single transformed df
# format_mvp takes the filepath for mvp file and formats it (drops a row, reduces columns)
# df_concat takes a list of file names and concatenates them

TEAM_ABB_DICT = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BRK': 'Brooklyn Nets',
    'CHO': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards',
    
    'SEA': 'Seattle SuperSonics',  # Became OKC in 2008
    'VAN': 'Vancouver Grizzlies',  # Became MEM in 2001
    'NJN': 'New Jersey Nets',  # Became BRK in 2012
    'NOH': 'New Orleans Hornets',  # Became NOP in 2013
    'NOK': 'New Orleans/Oklahoma City Hornets',  # 2005-2007
    'CHA': 'Charlotte Bobcats',  # Became CHO in 2014
    'WSB': 'Washington Bullets',  # Became WAS in 1997
}


def transform_plyr_dfs(pg_df, adv_df):
    pg_df['STL'] = pd.to_numeric(pg_df['STL'], errors='coerce')
    pg_df['BLK'] = pd.to_numeric(pg_df['BLK'], errors='coerce')
    pg_df['Stocks'] = round(pg_df[['STL','BLK']].sum(axis=1), 3)
    pg_df = pg_df[['Player','Team','G','PTS','AST','TRB','Stocks','eFG%']]

    adv_df = adv_df[['Player','Team','MP','PER','TS%','USG%','WS','BPM','VORP']]

    merged = pd.merge(pg_df, adv_df, on=['Player','Team'], how='left')
    merged['Team'] = merged['Team'].map(TEAM_ABB_DICT)
    merged['Team'] = merged.groupby('Player')['Team'].transform(lambda x:x.fillna(x.iloc[-1]))
    merged = merged.drop_duplicates(subset='Player', keep='first')
    return merged


def transform_team_df(df):
    df.columns = df.iloc[0]
    df = df.drop(df.index[0]).reset_index(drop=True)
    df['Team'] = df['Team'].str.replace('*','', regex=False)
    df['W'] = pd.to_numeric(df['W'])
    df['L'] = pd.to_numeric(df['L'])
    df['Team_Win%'] = round(df['W'] / (df['W'] + df['L']), 4)
    df['Team_G'] = df['W'] + df['L']
    return df[['Team','Team_Win%','Team_G']]


def transform_mvp_df(mvp_df) -> pd.DataFrame:
    '''MVP dataframe has unnecessary first row. This function drops the row, resets the index to the 2nd row, and only keeps a few columns'''
    mvp_df.columns = mvp_df.iloc[0]
    mvp_df = mvp_df.drop(mvp_df.index[0])
    mvp_df = mvp_df.reset_index(drop=True)
    mvp_df['Team'] = mvp_df['Tm'].map(TEAM_ABB_DICT)
    mvp_df = mvp_df[['Player','Team','Share']]
    return mvp_df


def load_data(final_path, week_path, mvp_pulled):
    path = final_path if mvp_pulled else week_path

    pg_df = pd.read_csv(path/'plyr_per_game.csv')
    adv_df = pd.read_csv(path/'plyr_advanced.csv')
    team_df = pd.read_csv(path/'adv_team_stats.csv')
    pie_df = pd.read_csv(path/'pie.csv')

    if mvp_pulled:
        mvp_df = pd.read_csv(final_path/'mvp.csv')
        return pg_df, adv_df, team_df, pie_df, mvp_df

    return pg_df, adv_df, team_df, pie_df


def transform_all(year):
    script_dir = Path(__file__).parent.resolve()
    repo_dir = script_dir.parent
    data_dir = Path(repo_dir/'data')
    raw_dir = data_dir/'raw'

    current_day = str(date.today())
    season_year = str(year)

    year_dir = raw_dir/season_year
    week_dir = year_dir/current_day
    final_path = year_dir/'final'

    json_path = Path(repo_dir/'seasons.json')
    json_file = load_json(json_path)

    season_over = json_file["seasons"][season_year]["season_over"]
    mvp_pulled = json_file["seasons"][season_year]["mvp_pulled"]

    if season_over and not mvp_pulled:
        print(f'{season_year} regular season over and MVP results are not yet known. Nothing to do, exiting...')
        return

    if mvp_pulled:
        print('MVP results have been obtained. Loading all 5 files...')
        pg_df, adv_df, team_df, pie_df, mvp_df = load_data(final_path, week_dir, mvp_pulled)

        mvp_df = transform_mvp_df(mvp_df)

    else:
        print('MVP results not obtained. Loading 4 files...')
        pg_df, adv_df, team_df, pie_df = load_data(final_path, week_dir, mvp_pulled)

    player_df = transform_plyr_dfs(pg_df, adv_df)
    team_df = transform_team_df(team_df)
    merged = pd.merge(player_df, team_df, on='Team', how='left')

    pie_df = pie_df[['PLAYER_NAME', 'PIE']].rename(columns={'PIE': 'pie'})
    merged = pd.merge(merged, pie_df, left_on='Player', right_on='PLAYER_NAME', how='left')
    merged = merged.drop(columns='PLAYER_NAME')
    merged['Year'] = int(season_year)
    
    if mvp_pulled:
        merged = pd.merge(merged, mvp_df, on=['Player','Team'], how='left')
        merged['Share'] = pd.to_numeric(merged['Share'], errors='coerce').fillna(0)
        merged['Games_Played_PCT'] = round(merged['G'] / merged['Team_G'], 4)
        merged['Award_eligible'] = np.where((merged['Games_Played_PCT'] > (60/82)) & (merged['MP'] >= 2000), 1, 0)
        merged = merged[merged['Award_eligible'] == 1]
        merged = merged.drop('Award_eligible', axis=1)
        #save file to processed dir for training
        make_directory(data_dir/'train')
        print('Saving transformed end of year (w/ MVP results) data to train/ folder')
        merged.to_parquet(data_dir/'train'/f'{season_year}.parquet')

    else:
        #save file to other dir for inference (model will be applied to this df since no mvp results)
        make_directory(data_dir/'inference'/season_year)
        print(f'Saving transformed weekly data to inference/{season_year}')
        merged.to_parquet(data_dir/'inference'/season_year/f'{current_day}.parquet')
