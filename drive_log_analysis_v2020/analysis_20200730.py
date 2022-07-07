import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/smart_drive_total/*.csv')
files = np.sort(files)
id_date_dict = {}
date_vec = []

id_date_dict = {}
total_date_set = set()
for file in files:
    print('*** ' + file + ' ***')
    df = pd.read_csv(file)
    # pdb.set_trace()
    id_set = set(df.user_id.dropna())
    for id in id_set:
        idx = np.where(df.user_id == id, True, False)
        df_sub = df.iloc[idx,:]
        timestamp_vec = df_sub.driving_started_at
        date_vec = np.array([timestamp.split(' ')[0] for timestamp in timestamp_vec])
        hour_vec = [timestamp.split(' ')[1] for timestamp in timestamp_vec]
        hour_vec = np.array([int(timestamp.split(':')[0]) for timestamp in hour_vec])
        # hour_vec = (hour_vec + 9)%24
        time_idx = np.where((hour_vec <= 2) | (21 <= hour_vec), True, False)
        date_set = set(date_vec[time_idx])
        total_date_set = total_date_set|set(date_vec)

        if id in id_date_dict:
            id_date_dict[id] = id_date_dict[id]|date_set
            # pdb.set_trace()
        else:
            id_date_dict[id] = date_set
datetime_vec = []
for timestamp in total_date_set:
    if 1 < len(timestamp.split('-')):
        tmp = timestamp.split('-')
        date_obj = datetime.datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        datetime_vec.append(date_obj)
datetime_vec = np.sort(datetime_vec)
delta = datetime_vec[len(datetime_vec)-1] - datetime_vec[0]
working_rate_vec = np.array([len(id_date_dict[id])/48 for id in id_date_dict.keys()])
pdb.set_trace()
