# this will run after tune.py, when the best parameters are found
# model is trained on all data prior to current year using best params, then saved as ../model/xgb_test_{year}.pkl

# ------------------------------------------------------------------------

import pandas as pd
import json
from pathlib import Path
from datetime import date

from xgboost import XGBRegressor
import pickle

# ------------------------------------------------------------------------

RECENT_SEASON = date.today().year

script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
train_dir = repo_dir/'data'/'train'

files = list(train_dir.glob('*.parquet')) #get all files in the training directory

df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
df = df[(df['PTS'] > 10) & (df['Team_Win%'] > 0.420) & (df['PER'] > 20)]

features = ['z_PTS','z_AST','z_TRB','z_Stocks','z_VORP','z_USG%','z_Team_Win%','z_eFG%','z_pie','PER']

with open(f'{repo_dir}/model/best_params_latest.json', 'r') as file:
    best_params = json.load(file)
print(f'Using the following params for model training: {best_params}')

df_train = df[df['Year'] < RECENT_SEASON]
X_train = df_train[features]
y_train = df_train['Share']

print('--Training XGBoost model--')
print('--------------------------')
final_model = XGBRegressor(**best_params, random_state=123)
final_model.fit(X_train, y_train)
print('XGBoost model trained!')

with open(f'{repo_dir}/model/xgb_test_{RECENT_SEASON}.pkl', 'wb') as f:
    pickle.dump(final_model, f)

print(f'Final model saved to ../model/xgb_test_{RECENT_SEASON}.pkl')