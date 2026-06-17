import time
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats


def get_data(year: int, table_type: str, trigger = None) -> pd.DataFrame:
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
    return df


def get_pie_feature(year:int) -> pd.DataFrame:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=year,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Advanced',
        timeout=60
    )

    df = stats.get_data_frames()[0]
    pie_df = df[['PLAYER_NAME','TEAM_ABBREVIATION','PIE']].sort_values('PIE', ascending=False)
    return pie_df