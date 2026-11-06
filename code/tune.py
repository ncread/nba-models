# this will run once per year to retrain the model!
# grabs all parquet files in data/train folder, so esure that has pulled the appropriate most recent finished season
# performs the time-series CV and tunes hyperparams to maximize spearmanr
# saves the best parameters to ../model/best_params_{year}.json and ../model/best_params_latest.json

# ------------------------------------------------------------------------

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date
from helpers import make_directory

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from scipy.stats import spearmanr
import optuna
import json

# ------------------------------------------------------------------------
RECENT_SEASON = date.today().year
print(f'The current year is {RECENT_SEASON}.')


def cv_metrics(df, features, params, target = 'Share'):
    '''return cross validation metrics for inputted training df, features, params. Train initially 1997-2006, then sequentially add a year.'''
    
    val_seasons = range(2007, RECENT_SEASON) 

    mae_list = []
    spearman_list = []

    for val_year in val_seasons:
        train_data = df[df['Year'] < val_year]
        val_data = df[df['Year'] == val_year]

        model = XGBRegressor(**params, random_state=123)
        model.fit(train_data[features], train_data[target])

        preds = model.predict(val_data[features])
        mae_list.append(mean_absolute_error(val_data[target], preds))
        spearman_list.append(spearmanr(val_data[target], preds)[0])

    return {'mae': np.mean(mae_list),
            'spearman': np.mean(spearman_list)}


def objective(trial):
    '''optuna function which provides starting point for hyperparameters. Returns the spearmanr value.'''

    params = {'n_estimators':     trial.suggest_int('n_estimators', 100, 600),
              'max_depth':        trial.suggest_int('max_depth', 2, 8),
              'learning_rate':    trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
              'subsample':        trial.suggest_float('subsample', 0.5, 1.0),
              'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
              'min_child_weight': trial.suggest_int('min_child_weight', 1, 20),
              'reg_alpha':        trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
              'reg_lambda':       trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True)
    }

    scores = cv_metrics(df, features, params, target='Share')
    return scores['spearman']


script_dir = Path(__file__).parent.resolve()
repo_dir = script_dir.parent
train_dir = repo_dir/'data'/'train'

files = list(train_dir.glob('*.parquet')) #get all files in the training directory

df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
df = df[(df['PTS'] > 10) & (df['Team_Win%'] > 0.420) & (df['PER'] > 20)]

features = ['z_PTS','z_AST','z_TRB','z_Stocks','z_VORP','z_USG%','z_Team_Win%','z_eFG%','z_pie','PER']


#hyperparameter tuning
print('Tuning hyperparameters...')
print('-------------------------')
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=200, show_progress_bar=True)
best_params = study.best_params

print(f'Best Spearman: {study.best_value}')
print(f'Best Params: {best_params}')


ml_asset_path = repo_dir/'model'
make_directory(ml_asset_path)

with open(f'{ml_asset_path}/best_params_{RECENT_SEASON}.json', 'w') as f:
    json.dump(best_params, f)

with open(f'{ml_asset_path}/best_params_latest.json', 'w') as f:
    json.dump(best_params, f) 
print(f'Best Params saved to ../model/best_params{RECENT_SEASON}.json and ../model/best_params_latest.json')