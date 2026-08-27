<h1 style="color:blue; text-align:center">NBA MVP Prediction Modeling</h1>

[![Run fetch_mvp.py](https://github.com/ncread/nba-models/actions/workflows/fetch_mvp.yaml/badge.svg?branch=main)](https://github.com/ncread/nba-models/actions/workflows/fetch_mvp.yaml)
[![Run fetch_weekly.py](https://github.com/ncread/nba-models/actions/workflows/fetch_weekly.yaml/badge.svg?branch=main)](https://github.com/ncread/nba-models/actions/workflows/fetch_weekly.yaml)
<!-- <div style="display:flex; justify-content:center; align-items:center">
    <img style="text-align:center" src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWhibzNzNzkzOTNpMjRrN3hkdTdpaDdmcXVyZGYxaHk5ZnZlM255dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kGuwoQZRC2eTeYgtN2/giphy.gif" alt="Scotty Waving">
</div>
<br> -->

## Overview
<div style="display:flex">
    <img src="https://media3.giphy.com/media/v1.    Y2lkPTc5MGI3NjExM2o2NjM1b3ZpYTNqeXU3dDB1ZzNwMjB6Z2EyenJjZWhhanJ0b2FyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Ph7nbx5SKE6bwnc3fj/giphy.gif" alt="DRose dunking on Dragic">
    <p style="margin-left:10px; font-size:16px">Every year during the NBA season, MVP standings are a hot topic, especially since journalists and broadcasters vote on the award and can publicly converse about it throughout the season. Just as professional basketball is a game of runs, so too is the MVP race. In mid-December when the season-ending award conversation starts to (prematurely?) heat up, players have really only played roughly two months' worth of games, making the progression of MVP predictions throughout the remainder of the season so compelling to follow. <br><br> This project leverages machine learning techniques to generate NBA MVP standings predictions trained on historical data sourced from Basketball Reference. Data for the current season is acquired weekly (early Monday AM) and fed into models trained on MVP results from the 1997-previous seasons. <br><br> Model predictions can be found here (coming soon), displaying the week-to-week fluctuations in the predicted standings.</p>
</div>


## Project Structure
```bash
nba-models/
├── code
│   ├── bball_ref.py   <- contains function to grab data from bball reference pages, used in both 00 and 01 files
│   ├── 00_past_szn.py
│   ├── 01_current_szn.py
│   ├── 02_data_transformation.py
│   ├── 03_modeling.py
├── data
│   ├── concat_df.csv
│   ├── 1997
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── pie.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── df.csv
│   ├── ...
│   ├── 2025
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── pie.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── df.csv
│   └── 2026
│       ├── 2026-02-02
│       │   ├── adv_team_stats.csv
│       │   ├── pie.csv
│       │   ├── plyr_advanced.csv
│       │   ├── plyr_per_game.csv
│       │   └── df.csv
│       ├── ...
│       ├── mvp_predictions.csv
│       ├── adv_team_stats.csv
│       ├── mvp.csv
│       ├── pie.csv
│       ├── plyr_advanced.csv
│       ├── plyr_per_game.csv
│       └── df.csv
├── .github
│   └── workflows
│       ├── run_00_past_szn.yaml
│       └── run_01_02_files.yaml
├── pyproject.toml
├── README.md
└── uv.lock
```

## Feature Origin & Engineering
Initial set of features are grabbed from either [Basketball Reference](https://www.basketball-reference.com/) or [the official NBA website](https://www.nba.com/):


| Origin | Features |  
|-----------|---------|
| BBall Ref | pts, ast, trb, stocks (stl+blk), eFG%, MP, PER, TS%, USG%, WS, BPM, VORP, Team Win % |
| NBA.com | PIE (player impact estimate) |

Prior to modeling, correlations between features were analyzed and decisions were made to ensure that highly correlated variables were not both included.
<br>
Typically for tree-based algorithms, the benefit to scaling the data lies in lower computational costs rather than ensuring features are on the same scale. In this case with data "grouped" by season, standardization using season-specific z-scores plays a bigger role. Z-score standardization essentially corrects for dynamic feature distributions, which for our purposes reduces the impact of the significant temporal shifts in offensive production that the NBA has seen over the last decade plus. This project initially was going to include data tracking all the way back to 1975, but decisions and adjustements were made to begin with the 1996-97 season. Even with the adjusted time period, we can still see significant increases in stats over the last 30 years.
