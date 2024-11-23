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


notification_type_translation = {1: "POST", 2: "REMOVED"}
cancel_reason_translation = {
    1: "CLICK", 2: "CANCEL", 3: "CANCEL_ALL", 4: "ERROR", 5: "PACKAGE_CHANGED", 
    6: "USER_STOPPED", 7: "PACKAGE_BANNED", 8: "APP_CANCEL", 9: "APP_CANCEL_ALL", 10: "LISTENER_CANCEL",
    11: "LISTENER_CANCEL_ALL", 12: "GROUP_SUMMARY_CANCELED", 13: "GROUP_OPTIMIZATION", 14: "PACKAGE_SUSPENDED", 15: "PROFILE_TURNED_OFF",
    16: "UNAUTOBUNDLED", 17: "CHANNEL_BANNED", 18: "SNOOZED", 19: "TIMEOUT"}


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
    
        if ("Notification" in date_data) and (uuid in date_data["Notification"]):
            for save_time, raw_instances in date_data["Notification"][uuid].items():
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
                        del instance['time']

                        if model=="Notification":
                            instance['type'] = translate(instance['type'], notification_type_translation)
                            if instance['type'] == "REMOVED":
                                instance['cancelReason'] = translate(instance['cancelReason'], cancel_reason_translation)
                        processed_instances.append({**empty_dict, **instance})

    df = DataFrame(processed_instances)
    return df.drop_duplicates()


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
        df = df.drop_duplicates()
        columns = df.columns
        key_columns = ['id', 'uuid', 'datetime']
        data_columns = columns.drop(key_columns)
        sorted_columns = Index(key_columns).append(data_columns)
        sorted_df = df[sorted_columns].sort_values(by=key_columns)
    else:
        sorted_df = df
    return sorted_df