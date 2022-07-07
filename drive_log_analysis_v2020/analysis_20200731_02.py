import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/smart_drive_total/*.csv')
files = np.sort(files)
date_id_dict = {}

total_user_id = set()
for file in files:
    print('*** ' + file + ' ***')
    df = pd.read_csv(file)
    # pdb.set_trace()
    timestamp_set = set(df.driving_started_at.dropna())
    for timestamp in timestamp_set:
        idx = np.where(df.driving_started_at == timestamp, True, False)
        df_sub = df.iloc[idx,:]

        date = timestamp.split(' ')[0]
        tmp = timestamp.split(' ')[1]
        hour = int(tmp.split(':')[0])
        user_id = df_sub.user_id.iloc[0]
        total_user_id.add(user_id)

        if hour <= 2 or 21 <= hour:
            if date in date_id_dict:
                if not user_id in date_id_dict[date]:
                    date_id_dict[date].append(user_id)
            else:
                date_id_dict[date] = [user_id]

working_rate_vec = np.array([len(date_id_dict[date])/len(total_user_id) for date in date_id_dict.keys()])
pdb.set_trace()
