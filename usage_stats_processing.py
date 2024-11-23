import re
import json
from itertools import chain

from datetime import datetime
from datetime import date, timedelta, time

from multiprocessing import Pool
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Index
from tqdm.notebook import tqdm
from utils import UUID2ID_DICT, UUIDS, IDS


def uuid2id(uuid):
    return UUID2ID_DICT[uuid]


def convertMillis(millis):
    seconds=(millis/1000)%60
    minutes=(millis/(1000*60))%60
    hours=(millis/(1000*60*60))%24
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def get_unit_dataframe(uuid, model):
    """
    Parse all data instances of a user and a model.
    """
    data_directory = Path('./data/')
    data_files = [file for file in data_directory.glob('uw-drg-default-rtdb-2023*') if file.is_file()]
        
    processed_instances = []
        
    for data_file in data_files:
        with open(data_file, 'r') as fp:
            date_data = json.load(fp)
            
        pattern = r'(\d{4}-\d{2}-\d{2})'

        match = re.search(pattern, data_file.name)
        
        if match:
            date = match.group(1)
        else:
            print(data_file.name)
            print("Date not found in the file name.")    
            
        id_ = uuid2id(uuid)

#         print(f"Processing for {uuid} on {date}")

        if uuid in date_data["UsageStats"]:
            for save_time, raw_instances in date_data["UsageStats"][uuid].items():
                if raw_instances == 'empty':
                    continue
                else:
                    for instance in raw_instances:
                        empty_dict = {
                            'uuid': uuid,
                            'id': id_,
                        }
                        if 'time' not in instance:
                            print(instance)
                            continue
                        dt = datetime.fromtimestamp(instance['time']/1000)
                        instance['date'] = date
                        instance['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                        if 'firstTimeStamp' in instance:
                            instance['firstTimeStamp'] = datetime.fromtimestamp(instance['firstTimeStamp']/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            instance['firstTimeStamp'] = ''
                        if 'lastTimeStamp' in instance:
                            instance['lastTimeStamp'] = datetime.fromtimestamp(instance['lastTimeStamp']/1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            instance['lastTimeStamp'] = ''
                        if 'totalTimeVisible' in instance:
                            instance['totalTimeVisible'] = convertMillis(instance['totalTimeVisible'])
                        else:
                            instance['totalTimeVisible'] = ''
                        if 'totalTimeForeground' in instance:
                            instance['totalTimeForeground'] = convertMillis(instance['totalTimeForeground'])
                        else:
                            instance['totalTimeForeground'] = ''
                        del instance['time']
                        processed_instances.append({**empty_dict, **instance})
    
    df = DataFrame(processed_instances)
    return df.drop_duplicates()


def get_uuid_model_dataframe(uuid, model):
    """
    Parse all data instances of a specific user and a specific model.
    """
    dataframes = get_unit_dataframe(uuid, model)
    return dataframes
    

def process_data(args):
    return get_uuid_model_dataframe(*args)
    
    
def get_model_dataframe(model):
    """
    Parse all data instances of a specific model.
    """
    args = [(uuid, model) for uuid in UUIDS]

    with Pool() as pool:
        dataframes = pool.starmap(get_uuid_model_dataframe, args)
    df = pd.concat(dataframes, axis=0, sort=False)
    columns = df.columns
    key_columns = ['id', 'uuid', 'datetime']
    data_columns = columns.drop(key_columns)
    sorted_columns = Index(key_columns).append(data_columns)
    sorted_df = df[sorted_columns].sort_values(by=key_columns, ascending=True)
    df = df.drop_duplicates()
    return sorted_df