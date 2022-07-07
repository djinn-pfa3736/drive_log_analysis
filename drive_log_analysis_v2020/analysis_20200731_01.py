import numpy as np
import matplotlib.pyplot as plt

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/dataset_sub/*.json')
files = np.sort(files)
date_id_dict = {}
car_id_set = set()

for file in files:
    print("*** " + file + " ***")
    tmp = file.split('/')[3]
    date = tmp.split('_')[0]

    with open(file) as f:
        df = json.load(f)

    items = df['Items']

    for item in items:
        hour_timestamp = item['timestamp'] % (60*60*24)
        hour = np.floor(hour_timestamp/(60**2))
        hour = (hour + 9) % 24

        car_id_set.add(item['car_id'])
        if hour <= 2 or 21 <= hour:
            if date in date_id_dict:
                if not item['car_id'] in date_id_dict[date]:
                    date_id_dict[date].append(item['car_id'])
            else:
                date_id_dict[date] = [item['car_id']]

working_rate_vec = np.array([len(date_id_dict[date]) for date in date_id_dict.keys()])/len(car_id_set)
pdb.set_trace()
