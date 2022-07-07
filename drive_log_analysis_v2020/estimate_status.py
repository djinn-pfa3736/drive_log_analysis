import numpy as np
import matplotlib.pyplot as plt

import folium

import datetime

import json
import glob

import pdb

def convert_date(timestamp):
    origin = datetime.datetime(1970, 1, 1)
    days = np.floor(timestamp/(60*60*24))
    residual = timestamp%(60*60*24)
    hours = np.floor(residual/(60*60))
    residual = residual%(60*60)
    minutes = np.floor(residual/60)
    seconds = float(residual%60)

    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    return delta + origin

id_lat_dict = {}
id_lng_dict = {}
id_time_dict = {}
files = glob.glob('dataset/dataset_sub/2020-07-07_*.json')
for file in files:
    with open(file) as f:
        df = json.load(f)

    items = df['Items']
    for item in items:
        id = item['car_id']

        if id in id_lat_dict:
            id_lat_dict[id].append(item['lat'])
            id_lng_dict[id].append(item['lng'])
            id_time_dict[id].append(item['timestamp'])
        else:
            id_lat_dict[id] = [item['lat']]
            id_lng_dict[id] = [item['lng']]
            id_time_dict[id] = [item['timestamp']]

car_id_set = id_lat_dict.keys()
for car_id in car_id_set:
    traj_lat = np.array(id_lat_dict[car_id])
    traj_lng = np.array(id_lng_dict[car_id])
    traj_time = np.array(id_time_dict[car_id])

    diff_lat = (traj_lat[1:len(traj_lat)] - traj_lat[0:(len(traj_lat)-1)])*100000
    diff_lng = (traj_lng[1:len(traj_lng)] - traj_lng[0:(len(traj_lng)-1)])*100000
    diff_time = (traj_time[1:len(traj_time)] - traj_time[0:(len(traj_time)-1)])

    v_vec = np.round(np.sqrt(diff_lat**2 + diff_lng**2)/diff_time, 3)
    total_v_vec = []
    for i in range(0, len(v_vec)):
        total_v_vec += [v_vec[i]]*diff_time[i]
    pdb.set_trace()
