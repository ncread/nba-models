# xgb_prod_latest.pkl is the most recently trained model using all past data
# looks in the inference folder for current season, looks for file from today's date, else uses the most recent inference file in the folder
# applies model to data to get predictions

# ------------------------------------------------------------------------

import pandas as pd
from pathlib import Path
from datetime import date
import pickle
import json

from helpers import make_directory, load_json, save_json

# ------------------------------------------------------------------------

def fetch_latest_inference(current_day: str, year_dir: Path) -> pd.DataFrame:

    target_file = f'{current_day}.parquet'
    weekly_file_dir = year_dir/target_file

    inference_files = list(year_dir.glob('*.parquet'))
    latest_inference = max([f for f in inference_files], key=lambda item: item.stat().st_ctime)

    try:
        df = pd.read_parquet(weekly_file_dir)
        print(f'Grabbed inference parquet file for {current_day}')
    except: # data may have been processed into inference folder, but this file may be running on a future date. Read the latest inference file present instead.
        print(f'Most recent inference file processing did not occur on {current_day}. Fetching {latest_inference}, the most recent inference file available...')
        df = pd.read_parquet(latest_inference)

    return df, latest_inference


def fetch_model(model_dir: Path):
    with open(model_dir, 'rb') as file:
        model = pickle.load(file)

    return model


SEASON_YEAR = (pd.Timestamp.now() + pd.DateOffset(months=3)).year 
current_day = str(date.today())

script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
data_dir = repo_dir/'data'
train_dir = data_dir/'train'
inference_dir = repo_dir/'data'/'inference'

year_dir = inference_dir/str(SEASON_YEAR)


# fetch latest model
latest_model = f'xgb_prod_{SEASON_YEAR-1}.pkl'

model_dir = repo_dir/'model'/latest_model
model = fetch_model(model_dir)
print('Model loaded...', end='')

# fetch latest inference data
df, latest_inf_file = fetch_latest_inference(current_day, year_dir)
features = ['z_PTS','z_AST','z_TRB','z_Stocks','z_VORP','z_USG%','z_Team_Win%','z_eFG%','z_pie','PER']
X_test = df[features]

# apply model to inference data
preds = model.predict(X_test)

# prep df
disp_df = df.copy()
disp_df['pred_mvp_share'] = preds
disp_df['raw_mvp_rank'] = disp_df['pred_mvp_share'].rank(ascending=False, method='first').astype(int)
disp_df['model_used'] = model_dir.stem
disp_df['pred_date'] = latest_inf_file.stem

print('MVP Predictions made...')

# print('-----Highest 20 Share Predictions------')
# print(disp_df.nlargest(20, 'pred_mvp_share')) #[['Player','pred_mvp_share']])

make_directory(data_dir/'predictions'/'df')

disp_df.to_parquet(f'{data_dir}/predictions/df/{latest_inf_file.stem}.parquet')


# apply cutoff filters prior to json construction, only if we're >=20 games into the season
top10_df = disp_df.copy()
filter_flag = 0

if top10_df['G'].max() > 20:
    print('The season is more than 20 games in, so w/ a robust sample size, we will filter the population...')
    print('Players must have the following: >10 PPG, >0.420 Team Win %, >20 PER')
    top10_df = top10_df[(top10_df['PTS'] > 10) & (top10_df['Team_Win%'] > 0.420) & (top10_df['PER'] > 20)]
    filter_flag = 1

top10_df['filt_mvp_rank'] = top10_df['pred_mvp_share'].rank(ascending=False, method='first').astype(int)
top10 = top10_df.nsmallest(10, 'filt_mvp_rank')
top10['pred_mvp_share'] = top10['pred_mvp_share'].astype('float64').round(4)
top10['Team_Win%'] = top10['Team_Win%'].round(3)

print('------Top 10 MVP Voter Share Predictions------')
print(top10)

preds_path = data_dir/'predictions'/'predictions.json'
preds_json = load_json(preds_path)

preds_json[latest_inf_file.stem] = {
    "filter_bool": filter_flag,
    "predictions": top10[['Player','Team','G','Team_G','MPG','PTS','AST','TRB','Stocks','eFG%','PER','TS%','USG%','WS','VORP','Team_Win%','pie','pred_mvp_share','filt_mvp_rank']].to_dict(orient='records'),
}

save_json(preds_json, preds_path)