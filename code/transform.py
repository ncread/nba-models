import sys
import pandas as pd
from pathlib import Path
pd.set_option('future.no_silent_downcasting', True)
sys.path.insert(0, Path(__file__).parent.resolve())

from helpers import make_directory, save_data


#transform the raw data and save output to processed folder within data folder
# feature_trans takes in the year directory and outputs a single transformed df
# format_mvp takes the filepath for mvp file and formats it (drops a row, reduces columns)
# df_concat takes a list of file names and concatenates them
