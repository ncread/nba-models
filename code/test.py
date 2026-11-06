# this will run after train.py
# calls in xgb_test_{year}.pickle from train.py
# I will check out resulting spearman and mae values before training model for production
    # if results aren't good, need to troubleshoot & fix before production training

# ------------------------------------------------------------------------

import pandas as pd
from pathlib import Path
from datetime import date

from sklearn.metrics import mean_absolute_error
from scipy.stats import spearmanr
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

with open(f'{repo_dir}/model/xgb_test_{RECENT_SEASON}.pkl','rb') as f:
    final_model = pickle.load(f)

df_test = df[df['Year'] == RECENT_SEASON]
X_test = df_test[features]
y_test = df_test['Share']

test_preds = final_model.predict(X_test)
test_mae = mean_absolute_error(y_test, test_preds)
test_spearman, _ = spearmanr(y_test, test_preds)

print(f'Test MAE: {test_mae}')
print(f'Test Spearman: {test_spearman}')

df_test = df_test.copy()
df_test['predicted'] = test_preds

print('\n Predicted Top 15:')
print(df_test.nlargest(15, 'predicted')[['Player','predicted','Share']])
print('\n Actual Top 10:')
print(df_test.nlargest(10, 'Share')[['Player','Share']])