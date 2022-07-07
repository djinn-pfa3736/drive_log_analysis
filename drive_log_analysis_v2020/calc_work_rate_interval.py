import numpy as np
import matplotlib.pyplot as plt

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/car-location-logs/2020-09-*.json')
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
        date_object = datetime.timedelta(seconds=item['timestamp']) + datetime.datetime(1970, 1, 1)
        hour = (date_object.hour + 9) % 24

        # pdb.set_trace()

        if hour <= 2 or 20 <= hour:
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
working_rate_vec = [len(id_date_dict[key])/float(len(date_set)) for key in id_date_dict.keys()]

pdb.set_trace()
