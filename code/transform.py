import sys
import pandas as pd
from pathlib import Path
pd.set_option('future.no_silent_downcasting', True)
sys.path.insert(0, Path(__file__).parent.resolve())

from helpers import make_directory, save_data

#want to loop through the year dirs and check for "transformed.csv" or whatever it will be called. if present, continue through the loop. If absent, check for the expected 5 files (4 + mvp file), and perform transformations if they're all present. If something is missing, call a function from fetch_historical to fetch it.
#transform the raw data and save output to processed folder within data folder
    #raw data comes from output from either the July mvp script, to transform the end of season stats as a training dataset (or just add the rows to an existing training set in the directory somewhere), OR the weekly script, where data is brought together into one df. Predictions are then made on this data based on the trained model from the previous season.
# feature_trans takes in the year directory and outputs a single transformed df
# format_mvp takes the filepath for mvp file and formats it (drops a row, reduces columns)
# df_concat takes a list of file names and concatenates them
