# NBA ML Prediction Modeling

(In development) A model generating MVP predictions and team playoff success using historical data (1975-previous season) from Basketball Reference.

## Overview

TBD

## Project Structure
```bash
nba-models/
├── code
│   ├── bball_ref.py
│   ├── 00_past_szn.py
│   ├── 01_current_szn.py
├── data
│   ├── 1975
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── opp_team_per_game.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── team_per_game.csv
│   ├── ...
│   ├── 2025
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── opp_team_per_game.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── team_per_game.csv
│   └── 2026
│       └── 2026-02-02
│           ├── adv_team_stats.csv
│           ├── opp_team_per_game.csv
│           ├── plyr_advanced.csv
│           ├── plyr_per_game.csv
│           └── team_per_game.csv
│       └── ...
├── .github
│   └── workflows
│       ├── run_00_acquire_data.yaml
│       └── run_01_current_szn.yaml
├── pyproject.toml
├── README.md
└── uv.lock
