import numpy as np
import pandas as pd
from datetime import date
from pathlib import Path
pd.set_option('future.no_silent_downcasting', True)


##########################################################################

#this file will be run once per week (~6 AM Monday mornings) after 01_current_szn.py to capture changes to the data from previous week's games

##########################################################################


def feature_trans(year_dir: str, current_year_flag = False) -> pd.DataFrame:
    '''
    Takes a certain file path, calls in csv files and performs transformations and joins to output a new dataframe
    '''

    if current_year_flag:
        print(f'{year_dir} is the current season directory. Grabbing the most recent weekly data...', end=' ')
        current_year_dir = Path(f'{year_dir}')
        weekly_subfolders = sorted([f for f in current_year_dir.iterdir() if f.is_dir()])
        most_recent = weekly_subfolders[-1] if weekly_subfolders else None
        
        plyr_per_game = pd.read_csv(f'{most_recent}/plyr_per_game.csv')
        plyr_advanced = pd.read_csv(f'{most_recent}/plyr_advanced.csv')
        team_advanced = pd.read_csv(f'{most_recent}/adv_team_stats.csv')

    else:
        plyr_per_game = pd.read_csv(f'{year_dir}/plyr_per_game.csv')
        plyr_advanced = pd.read_csv(f'{year_dir}/plyr_advanced.csv')
        team_advanced = pd.read_csv(f'{year_dir}/adv_team_stats.csv')

    #plyr_per_game transformations
    plyr_per_game['Par'] = round(plyr_per_game[['PTS','AST','TRB']].sum(axis=1), 4)
    plyr_per_game['Stocks'] = round(plyr_per_game[['STL','BLK']].sum(axis=1), 3)
    plyr_avg_df = plyr_per_game[['Player','Team','G','Par','Stocks','eFG%']]

    plyr_adv_df = plyr_advanced[['Player','Team','PER','TS%','WS','BPM','VORP']]

    #merge two player dataframes
    plyr_merged = pd.merge(plyr_avg_df, plyr_adv_df, on=['Player','Team'], how='left')
    plyr_merged['Team'] = plyr_merged['Team'].map(team_abb_dict) #map abbrevs to full team names
    plyr_merged['Team'] = plyr_merged.groupby('Player')['Team'].transform(lambda x: x.fillna(x.iloc[-1])) #ensure cumulative stats show current team
    plyr_merged = plyr_merged.drop_duplicates(subset='Player', keep='first') #remove subsetted rows 

    #adv_team_stats tranformations
    team_advanced.columns = team_advanced.iloc[0]
    team_advanced = team_advanced.drop(team_advanced.index[0])
    team_advanced = team_advanced.reset_index(drop=True)
    team_advanced['Team'] = team_advanced['Team'].str.replace('*','')
    team_advanced['W'] = pd.to_numeric(team_advanced['W'])
    team_advanced['L'] = pd.to_numeric(team_advanced['L'])
    team_advanced['Team_Win%'] = round(team_advanced['W'] / (team_advanced['W'] + team_advanced['L']), 4)
    team_advanced['Team_G'] = team_advanced['W'] + team_advanced['L']
    team_adv_df = team_advanced[['Team','Team_Win%','Team_G']]

    #merge player & team dataframes
    df = pd.merge(plyr_merged, team_adv_df, on=['Team'], how='left')
    return df


def format_mvp(file_path: str) -> pd.DataFrame:
    mvp = pd.read_csv(file_path)
    mvp.columns = mvp.iloc[0]
    mvp = mvp.drop(mvp.index[0])
    mvp = mvp.reset_index(drop=True)
    mvp['Team'] = mvp['Tm'].map(team_abb_dict)
    mvp_df = mvp[['Player','Team','Share']]
    return mvp_df


def df_concatenation(df_file_names: list) -> pd.DataFrame:
    df_list = []
    for name in df_file_names:
            df = pd.read_csv(name)
            df_list.append(df)

    combined_df = pd.concat(df_list)
    return combined_df

#############################
team_abb_dict = {
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

script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
data_dir = Path(repo_dir/'data')

current_year = date.today().year
current_szn_dir = f'{data_dir}/2026' #will be changed when new season begins
#############################

past_df_list = []

#looping through data directory folders
for year_dir in data_dir.iterdir():

    if year_dir.is_dir(): # check to ensure iteration skips /data/df.csv file to avoid failure
        print(f'Starting {str(year_dir)[-4:]} processing.', end=' ')
    else:
        continue

    if str(year_dir) == current_szn_dir:
        df = feature_trans(year_dir, True)
        
    else:
        # comment out next 3 lines & rerun if change has been made to dataframe construction
        if Path(f'{year_dir}/df.csv').is_file(): #move on to next year if df.csv already exists
            print(f'Dataframe has already been constructed for {str(year_dir)[-4:]}. Proceeding to the next year...')
            continue

        df = feature_trans(year_dir)
        mvp_df = format_mvp(f'{year_dir}/mvp.csv')

        #merge mvp df features
        df = pd.merge(df, mvp_df, on=['Player','Team'], how='left')
        df['Share'] = df['Share'].fillna(0)
        df['Games_Played_PCT'] = round(df['G'] / df['Team_G'],4)
        df['Award_eligible'] = np.where(df['Games_Played_PCT'] > (65/82), 1, 0)
        df = df[df['Award_eligible'] == 1]
        df = df.drop('Award_eligible', axis=1)
        past_df_list.append(f'{year_dir}/df.csv')
    
    df['Year'] = str(year_dir)[-4:]

    #save df to csv
    df.to_csv(f'{year_dir}/df.csv') #contains all plyr and team features of interest, plus mvp voter share
    print(f'Successfully saved dataframe for {str(year_dir)[-4:]}')

df_concat = df_concatenation(past_df_list)
df_concat.to_csv(f'{data_dir}/df.csv')
print(f'Successfully concatenated dataframes from finished seasons: {data_dir}/df.csv')