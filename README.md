# NBA ML Prediction Modeling

[![Run 01_current_szn.py](https://github.com/ncread/nba-models/actions/workflows/run_01_02_files.yaml/badge.svg)](https://github.com/ncread/nba-models/actions/workflows/run_01_02_files.yaml)

(In development) A model generating NBA MVP standings predictions using historical data (1980-previous season) from Basketball Reference. Data for the current season is acquired weekly (Monday AM) and fed into machine learning models trained on the MVP results from previous seasons.

## Overview

TBD

## Project Structure
```bash
nba-models/
├── code
│   ├── bball_ref.py
│   ├── 00_past_szn.py
│   ├── 01_current_szn.py
│   ├── 02_data_transformation.py
├── data
│   ├── df.csv
│   ├── 1980
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
├── .github
│   └── workflows
│       ├── run_00_past_szn.yaml
│       └── run_01_02_files.yaml
├── pyproject.toml
├── README.md
└── uv.lock
