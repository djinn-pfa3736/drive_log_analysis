import numpy as np
import matplotlib.pyplot as plt

import folium

import json
import glob

import pdb

files = glob.glob('dataset/2020-07-car-position-history/2020-07-01_*.json')
id_dict_time = {}
id_dict_lat = {}
id_dict_lng = {}
for file in files:
    with open(file) as f:
        df = json.load(f)

    items = df['Items']
    for item in items:
        if item['car_id'] in id_dict_time:
            id_dict_time[item['car_id']].append(item['timestamp'])
            id_dict_lat[item['car_id']].append(round(item['lat'], 3))
            id_dict_lng[item['car_id']].append(round(item['lng'], 3))
        else:
            id_dict_time[item['car_id']] = [item['timestamp']]
            id_dict_lat[item['car_id']] = [round(item['lat'], 3)]
            id_dict_lng[item['car_id']] = [round(item['lng'], 3)]

id_dict_count = {}
for car_id in id_dict_time.keys():
    lat_list = id_dict_lat[car_id]
    lng_list = id_dict_lng[car_id]
    count_dict_lat_lng = {}
    for i in range(0, len(lat_list)):
        if (lat_list[i], lng_list[i]) in count_dict_lat_lng:
            count_dict_lat_lng[(lat_list[i], lng_list[i])] += 1
        else:
            count_dict_lat_lng[(lat_list[i], lng_list[i])] = 1
    id_dict_count[car_id] = count_dict_lat_lng

waiting_coords = []
color_list = []
for car_id in id_dict_count.keys():
    coords_dict = id_dict_count[car_id]

    if len(coords_dict) != 1:
        # pdb.set_trace()
        count = 0
        for key in coords_dict.keys():

            if count % 2 == 0:
                color_list.append('green')
            else:
                color_list.append('red')
            count += 1

            if 120 < coords_dict[key]:
                waiting_coords.append(key)

# pdb.set_trace()

# api_key = 'AIzaSyBDw21jOsimHpAueMaVrvdCTvj4OO1z50o'
m = folium.Map(location=[waiting_coords[0][0], waiting_coords[0][1]])
for i in range(0, len(waiting_coords)):
    coord = waiting_coords[i]
    print(str(coord[0]) + ',' + str(coord[1]))
    folium.Marker(location=[coord[0], coord[1]], icon=folium.Icon(color=color_list[i])).add_to(m)
m.save('waiting_locations.html')
# pdb.set_trace()
