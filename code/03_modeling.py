#training/validation set will be data/df.csv
#testing set will be 2026/df.csv (so 02_data_transformation file needs to be run after 01_current_szn is run every week to generate new predictions)
import pandas as pd
import numpy as np
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

historical_df = pd.read_csv(f'{data_dir}/df.csv')
design_matrix_feat = ['Par','Stocks','eFG%','PER','TS%','WS','BPM','VORP','Team_Win%']
X = historical_df[design_matrix_feat] #design matrix
y = historical_df['Share'] #prediction target

current_df = pd.read_csv(f'{data_dir}/{current_year}/df.csv')

current_df['Games_Played_PCT'] = round(current_df['G'] / current_df['Team_G'],4)
current_df = current_df[(current_df['Games_Played_PCT'] >= (0.75)) & (current_df['MP'] >= 1800)]
# print(current_df.head(25))
predicting_on_df = current_df[design_matrix_feat]


# ------------------------------------------------------------- #
#write function for model process here, then it can be applied to datasets from different weeks
#just need to process each dataset prior to ensure it's ready for the model function
dtree_reg = DecisionTreeRegressor(random_state=1)
dtree_reg.fit(X, y)

resulting_df = current_df
resulting_df['Predictions'] = dtree_reg.predict(predicting_on_df)

# resulting_df.to_csv(f'{data_dir}/predictions_df.csv')

print(resulting_df.sort_values('Predictions', ascending=False).head(20))