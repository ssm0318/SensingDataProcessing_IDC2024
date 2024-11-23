# README.md

## Overview

This repository contains a collection of Python scripts and Jupyter notebooks for processing and analyzing mobile usage statistics and notifications data. 

### Files and Major Functionalities

#### 1. usage_stats_processing.py

This Python script processes usage statistics data. Key functionalities include:

- `uuid2id(uuid)`: Converts a given UUID to a corresponding user ID using a predefined dictionary.
- `convertMillis(millis)`: Converts time given in milliseconds to a time string formatted as 'HH:MM:SS'.
- `get_unit_dataframe(date, uuid, model)`: Given a date, user UUID, and model, returns a DataFrame consisting of processed data instances for that specific date, user, and model.
- `get_uuid_model_dataframe(uuid, model)`: Aggregates all data instances of a specific user and model across all dates into a DataFrame.
- `get_model_dataframe(model)`: Aggregates all data instances of a specific model across all users and dates into a DataFrame.

#### 2. Sanity Check - Usage Stats.ipynb

This Jupyter notebook performs a sanity check on the processed usage statistics data and conducts some basic exploratory analysis:

- Imports the `get_model_dataframe` function from `usage_stats_processing.py` script to load data.
- Defines a list of specific applications (`drg_apps`) for which the analysis will be conducted.
- Reads in the data and processes it to remove duplicates and sort it in order of date and timestamp.
- Filters out instances where both 'totalTimeForeground' and 'totalTimeVisible' are zero.
- Displays the first few records of the processed data.
- Filters and presents data for specific applications defined in `drg_apps`.

#### 3. notifications_processing.py

This Python script processes notification data. Main functionalities include:

- `uuid2id(uuid)`: Similar to the function in `usage_stats_processing.py`, it converts a given UUID to a corresponding user ID.
- `convertMillis(millis)`: Similar to the function in `usage_stats_processing.py`, it converts time given in milliseconds to a time string formatted as 'HH:MM:SS'.
- `get_unit_dataframe(date, uuid, model)`: Similar to the function in `usage_stats_processing.py`, it returns a DataFrame consisting of processed data instances for a specific date, user, and model. However, in this script, it focuses on processing notification data.
- `get_uuid_model_dataframe(uuid, model)`: Similar to the function in `usage_stats_processing.py`, it aggregates all data instances of a specific user and model across all dates into a DataFrame.
- `get_model_dataframe(model)`: Similar to the function in `usage_stats_processing.py`, it aggregates all data instances of a specific model across all users and dates into a DataFrame.

#### 4. Sanity Check - Notifications.ipynb

This Jupyter notebook performs a sanity check on the processed notification data:

- Imports the `get_model_dataframe` function from `notifications_processing.py` to load the data.
- Defines a list of specific applications (`drg_apps`) for which the analysis will be conducted.
- Displays the processed data.

## How to Use

Run the Python scripts (`usage_stats_processing.py` and `notifications_processing.py`) to generate and process the usage statistics and notification data. These scripts can be configured by modifying the UUID2ID_DICT and DATES as per your data. 

The processed data can then be further analyzed using the Jupyter notebooks (`Sanity Check - Usage Stats.ipynb` and `Sanity Check - Notifications.ipynb`), which utilize the functions defined in the respective scripts.

Remember to install all dependencies listed in the files, such as pandas, datetime, json, re, itertools, pathlib, tqdm, and multiprocessing:

```

bash
pip install pandas datetime json5 re itertools pathlib2 tqdm multiprocessing
```
# SensingDataProcessing_IDC2024
