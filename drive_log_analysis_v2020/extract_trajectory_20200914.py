import numpy as np
import matplotlib.pyplot as plt

import folium

import json
import glob

import datetime

import pdb

files = glob.glob('./dataset/car-location-logs/2020-09-11_*.json')
files = np.sort(files)
id_date_dict = {}
date_vec = []

hit_item_list = []
for file in files:
    print("*** " + file + " ***")
    tmp = file.split('/')[3]
    date = tmp.split('_')[0]
    date_vec.append(date)

    with open(file) as f:
        df = json.load(f)

    items = df['Items']
    """
    注文削除時間：2020-9-12, 1:30:32
    注文作成時間：2020-9-12, 1:07:57
    'car_id': 122, 'driver_id': 89
    TOM: 60, 'car_id': 131

    注文削除時間　2020-9-12, 4:03:40
    注文作成時間　2020-9-12, 3:43:05

    """

    for item in items:

        if item['car_id'] == 131:
        # if item['car_id'] == 48:
            hit_item_list.append(item)
            # pdb.set_trace()

        # if (hour == 1) & (minute == 30):
        #     pdb.set_trace()

result_item_list = []
time_list = []
get_flag = False
for item in hit_item_list:
    date_object = datetime.timedelta(seconds=item['timestamp']) + datetime.datetime(1970, 1, 1)
    hour = (date_object.hour + 9) % 24
    # hour = date_object.hour
    minute = date_object.minute
    second = date_object.second

    # print('%s %s %s' % (hour, minute, second))

    if (hour == 1) & (minute == 8) & (0 < second):
        get_flag = True

    if (hour == 1) & (minute == 30) & (32 < second):
        get_flag = False

    if get_flag:
        result_item_list.append(item)
        time_list.append((hour, minute, second))

lat_list = []
lng_list = []
for item in result_item_list:

    lat_list.append(item['lat'])
    lng_list.append(item['lng'])

lat_center = np.median(lat_list)
lng_center = np.median(lng_list)

m = folium.Map(location=[lat_center, lng_center], zoom_start=13)

for i in range(len(lat_list)-1):
    folium.PolyLine(locations=[[lat_list[i], lng_list[i]], [lat_list[i+1], lng_list[i+1]]]).add_to(m)

pdb.set_trace()
