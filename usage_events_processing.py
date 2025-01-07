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


# REFERENCE: https://developer.android.com/reference/android/app/usage/UsageEvents.Event


usage_event_type_translation = {
    0: "NONE",
    1: "ACTIVITY_RESUMED",
    2: "ACTIVITY_PAUSED",
    5: "CONFIGURATION_CHANGE",
    7: "USER_INTERACTION",
    8: "SHORTCUT_INVOCATION",
    11: "STANDBY_BUCKET_CHANGED",
    15: "SCREEN_INTERACTIVE",
    16: "SCREEN_NON_INTERACTIVE",
    17: "KEYGUARD_SHOWN",
    18: "KEYGUARD_HIDDEN",
    19: "FOREGROUND_SERVICE_START",
    20: "FOREGROUND_SERVICE_STOP",
    23: "ACTIVITY_STOPPED",
    26: "DEVICE_SHUTDOWN",
    27: "DEVICE_STARTUP",
}


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
    
        if ("UsageEvent" in date_data) and (uuid in date_data["UsageEvent"]):
            for save_time, raw_instances in date_data["UsageEvent"][uuid].items():
                if raw_instances == 'empty':
                    continue
                else:
                    for instance in raw_instances:
                        empty_dict = {
                            'uuid': uuid,
                            'id': id_,
                        }
                        if 'timeStamp' not in instance:
                            print(instance)
                            continue
                        try:
                            dt = datetime.fromtimestamp(instance['timeStamp']/1000)
                            instance['date'] = date
                            instance['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                            del instance['timeStamp']
                        except Exception as e:
                            print(e)
                            print(instance)

                        instance['eventType'] = translate(instance['eventType'], usage_event_type_translation)
                        processed_instances.append({**empty_dict, **instance})

    df = DataFrame(processed_instances)
#     return df.drop_duplicates()
    return df


def translate(instance, translation):
    NOT_DEFINED = 'NOT_DEFINED'
    if instance in translation.keys():
        instance = translation[instance]
    else:
        instance = NOT_DEFINED
    return instance


def get_uuid_model_dataframe(uuid, model):
    """
    Parse all data instances of a specific user and a specific model.
    """
    dataframes = get_unit_dataframe(uuid, model)
    return dataframes
    

def get_model_dataframe(model):
    """
    Parse all data instances of a specific model.
    """
    
    args = [(uuid, model) for uuid in UUIDS]
    with Pool() as pool:
        dataframes = pool.starmap(get_uuid_model_dataframe, args)
    df = pd.concat(dataframes, axis=0, sort=False)
    if len(df) > 0:
#         df = df.drop_duplicates()
        columns = df.columns
        key_columns = ['id', 'uuid', 'datetime']
        data_columns = columns.drop(key_columns)
        sorted_columns = Index(key_columns).append(data_columns)
        sorted_df = df[sorted_columns].sort_values(by=key_columns)
    else:
        sorted_df = df
    return sorted_df