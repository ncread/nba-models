#training/validation set will be data/df.csv
#testing set will be 2026/df.csv (so 02_data_transformation file needs to be run after 01_current_szn is run every week to generate new predictions)
import pandas as pd
from pathlib import Path
from datetime import date
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression


script_dir = Path(__file__).parent.resolve() # /home/noah/Documents/projects/nba/code
repo_dir = script_dir.parent
data_dir = Path(repo_dir/'data')

current_year = date.today().year

# ------------------------------------------------------------- #

historical_df = pd.read_csv(f'{data_dir}/merged/df.csv')
design_matrix_feat = ['Par','Stocks','eFG%','PER','TS%','WS','BPM','VORP','Team_Win%']
X = historical_df[design_matrix_feat] #design matrix
y = historical_df['Share'] #prediction target

current_df = pd.read_csv(f'{data_dir}/{current_year}/df.csv')
predicting_on_df = current_df[design_matrix_feat]



dtree_reg = DecisionTreeRegressor(random_state=1)
dtree_reg.fit(X, y)

resulting_df = current_df
resulting_df['Predictions'] = dtree_reg.predict(predicting_on_df)

resulting_df.to_csv(f'{data_dir}/predictions_df.csv')

res = resulting_df[(resulting_df['Team_G'] - resulting_df['G']) <= 17]
print(res.sort_values('Predictions', ascending=False).head(15))