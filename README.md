# NBA ML Prediction Modeling

A model generating MVP predictions and team playoff success using historical data (1975-previous season) from Basketball Reference.

## Overview

TBD

## Project Structure
```bash
nba-models/
├── 00_acquire_data.py
├── data
│   ├── 1975
│   │   ├── adv_team_stats.csv
│   │   ├── mvp.csv
│   │   ├── opp_team_per_game.csv
│   │   ├── plyr_advanced.csv
│   │   ├── plyr_per_game.csv
│   │   └── team_per_game.csv
│   ├── ...
│   │
│   └── 2025
│       ├── adv_team_stats.csv
│       ├── mvp.csv
│       ├── opp_team_per_game.csv
│       ├── plyr_advanced.csv
│       ├── plyr_per_game.csv
│       └── team_per_game.csv
├── run_00_acquire_data.yaml
├── pyproject.toml
├── README.md
└── uv.lock
