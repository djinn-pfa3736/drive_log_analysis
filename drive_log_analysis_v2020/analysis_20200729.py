import numpy as np
import matplotlib.pyplot as plt

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/dataset_sub/*.json')
files = np.sort(files)
id_date_dict = {}
date_vec = []

for file in files:
    print("*** " + file + " ***")
    tmp = file.split('/')[3]
    date = tmp.split('_')[0]
    date_vec.append(date)

    with open(file) as f:
        df = json.load(f)

    items = df['Items']

    for item in items:
        hour_timestamp = item['timestamp'] % (60*60*24)
        hour = np.floor(hour_timestamp/(60**2))
        hour = (hour + 9) % 24

        if hour <= 2 or 21 <= hour:
            if item['car_id'] in id_date_dict:
                if not date in id_date_dict[item['car_id']]:
                    id_date_dict[item['car_id']].append(date)
            else:
                id_date_dict[item['car_id']] = [date]

        """
        if item['car_id'] in id_date_dict:
            if not date in id_date_dict[item['car_id']]:
                id_date_dict[item['car_id']].append(date)
        else:
            id_date_dict[item['car_id']] = [date]
        """

date_set = set(date_vec)
working_rate_vec = [len(id_date_dict[key])/len(date_set) for key in id_date_dict.keys()]

pdb.set_trace()
