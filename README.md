<h1 style="color:blue; text-align:center">NBA MVP Prediction Modeling</h1>

[![Run 01_current_szn.py](https://github.com/ncread/nba-models/actions/workflows/run_01_02_files.yaml/badge.svg)](https://github.com/ncread/nba-models/actions/workflows/run_01_02_files.yaml)


## Overview
<div style="display:flex">
    <img src="https://media3.giphy.com/media/v1.    Y2lkPTc5MGI3NjExM2o2NjM1b3ZpYTNqeXU3dDB1ZzNwMjB6Z2EyenJjZWhhanJ0b2FyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Ph7nbx5SKE6bwnc3fj/giphy.gif" alt="DRose dunking on Dragic">
    <p style="margin-left:10px; font-size:16px">Every year during the NBA season, MVP standings are a hot topic, especially since journalists and broadcasters vote on the award and can publicly converse about it throughout the season. Just as professional basketball is a game of runs, so too is the MVP race. In mid-December when the season-ending award conversation starts to (prematurely?) heat up, players have really only played roughly two months' worth of games, making the progression of MVP predictions throughout the remainder of the season so compelling to follow. <br><br> This project leverages machine learning techniques to generate NBA MVP standings predictions trained on historical data sourced from Basketball Reference. Data for the current season is acquired weekly (early Monday AM) and fed into models trained on MVP results from the 1997-previous seasons. <br><br> Model predictions can be found here (coming soon), displaying the week-to-week fluctuations in the predicted standings.</p>
</div>


## Project Structure
```bash
nba-models/
├── code
│   ├── bball_ref.py
│   ├── 00_past_szn.py
│   ├── 01_current_szn.py
│   ├── 02_data_transformation.py
│   ├── 03_modeling.py
├── data
│   ├── concat_df.csv
│   ├── 1997
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── opp_team_per_game.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── team_per_game.csv
│   │   └── df.csv
│   ├── ...
│   ├── 2025
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── opp_team_per_game.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── team_per_game.csv
│   │   └── df.csv
│   └── 2026
│       └── 2026-02-02
│           ├── adv_team_stats.csv
│           ├── opp_team_per_game.csv
│           ├── plyr_advanced.csv
│           ├── plyr_per_game.csv
│           └── team_per_game.csv
│           └── df.csv
│       └── ...
│       └── mvp_predictions.csv
├── .github
│   └── workflows
│       ├── run_00_past_szn.yaml
│       └── run_01_02_files.yaml
├── pyproject.toml
├── README.md
└── uv.lock
```

## Features and Model Selection
Coming soon.
