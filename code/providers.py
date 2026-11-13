import time
import pandas as pd
import unicodedata
from nba_api.stats.endpoints import leaguedashplayerstats


def get_bballref(year: int, table_type: str, trigger = None) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

    if trigger == 'mvp':
        url = f'https://www.basketball-reference.com/awards/awards_{year}.html#all_mvp'

    elif trigger == 'team':
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'

        tables = pd.read_html(url, storage_options=headers)
        time.sleep(3)
        if year > 2015: #basketball reference began including conference standings in 2016, altering webpage structure
            #team_per_game = tables[4]
            #opp_per_game = tables[5]
            adv_team_stats = tables[10]
        else:
            #team_per_game = tables[2]
            #opp_per_game = tables[3]
            adv_team_stats = tables[8]

        # return (team_per_game, opp_per_game, adv_team_stats)
        return adv_team_stats
    else:
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_{table_type}.html'


    tables = pd.read_html(url, storage_options=headers)
    time.sleep(3)
    df = tables[0]
    df['Player'] = df['Player'].astype(str).apply(lambda s: unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('utf-8'))
    return df


def get_nba(year: str) -> pd.DataFrame:
    for attempt in range(3):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/124.0 Safari/537.36',
                'Referer': 'https://www.nba.com/',
                'Origin': 'https://www.nba.com',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'x-nba-stats-origin': 'stats',
                'x-nba-stats-token': 'true',
            }
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=year,
                season_type_all_star='Regular Season',
                per_mode_detailed='PerGame',
                measure_type_detailed_defense='Advanced',
                headers=headers,
                timeout=30
            )

            df = stats.get_data_frames()[0]
            break

        except Exception as e:
            print(f'Attempt {attempt} error: e')
            time.sleep(5)            

    pie_df = df[['PLAYER_NAME','TEAM_ABBREVIATION','PIE']].sort_values('PIE', ascending=False)
    pie_df['PLAYER_NAME'] = df['PLAYER_NAME'].astype(str).apply(lambda s: unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('utf-8'))
    return pie_df