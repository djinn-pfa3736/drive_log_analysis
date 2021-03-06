import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys

import json
import glob
import pickle

import datetime

import folium

import pdb

def convert_timestamp_to_string(timestamp):
    days = np.floor(timestamp/(60*60*24))
    res = timestamp%(60*60*24)
    hours = np.floor(res/(60*60))
    res = res%(60*60)
    minutes = np.floor(res/60)
    seconds = res%60

    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    origin = datetime.datetime(1970, 1, 1)
    current = origin + delta

    time_string = str(current.year) + '-' + str(current.month) + '-' + str(current.day) + 'T'
    time_string = time_string + str(current.hour) + ':' + str(current.minute) + ':' + str(current.second) + 'Z'

    return time_string

def compare_time_string(time_string0, time_string1):
    tmp0 = time_string0.split('T')
    tmp1 = time_string1.split('T')
    date0 = tmp0[0]
    date1 = tmp1[0]
    tmp0 = tmp0[1].split(':')
    tmp1 = tmp1[1].split(':')
    hour0 = int(tmp0[0])
    hour1 = int(tmp1[0])
    minute0 = int(tmp0[1])
    minute1 = int(tmp1[1])
    second0 = int(tmp0[2].split('Z')[0])
    second1 = int(tmp1[2].split('Z')[0])

    date_tmp0 = date0.split('-')
    date_tmp1 = date1.split('-')
    datetime0 = datetime.datetime(int(date_tmp0[0]), int(date_tmp0[1]), int(date_tmp0[2]), hour0, minute0, second0)
    datetime1 = datetime.datetime(int(date_tmp1[0]), int(date_tmp1[1]), int(date_tmp1[2]), hour1, minute1, second1)

    delta = datetime0 - datetime1
    if delta.days < 0:
        delta = datetime1 - datetime0

    return delta.seconds

file_header = sys.argv[1]
csv_file = sys.argv[2]
date_string = sys.argv[3]

df = pd.read_csv(csv_file)

json_car_id_vec = []
json_time_vec = []
json_timestamp_vec = []
json_lat_vec = []
json_lng_vec = []
files = glob.glob(file_header + date_string + '_*.json')
for file in files:
    with open(file) as f:
        df_json = json.load(f)
    items = df_json['Items']
    for item in items:
        json_car_id_vec.append(item['car_id'])
        time_string = convert_timestamp_to_string(item['timestamp'])
        json_time_vec.append(time_string)
        json_timestamp_vec.append(item['timestamp'])
        json_lat_vec.append(item['lat'])
        json_lng_vec.append(item['lng'])

sorted_arg = np.argsort(json_timestamp_vec)
json_timestamp_vec = np.array(json_timestamp_vec)[sorted_arg]
json_time_vec = np.array(json_time_vec)[sorted_arg]
json_lat_vec = np.array(json_lat_vec)[sorted_arg]
json_lng_vec = np.array(json_lng_vec)[sorted_arg]
json_car_id_vec = np.array(json_car_id_vec)[sorted_arg]

timestamp_vec = df.iloc[:,2]
date_vec = np.array([timestamp.split('T')[0] for timestamp in timestamp_vec])
date_idx = np.where(date_vec == date_string, True, False)

df_sub = df.iloc[date_idx,:]
car_id_set = set(df_sub.iloc[:, 1].dropna())

for car_id in car_id_set:
    print("*** " + date_string + " ***")
    car_id_idx = np.where(df_sub.iloc[:, 1] == car_id, True, False)
    df_id = df_sub.iloc[car_id_idx,:]

    approaching_idx = np.where(df_id.iloc[:,6] == 'approaching', True, False)
    arriving_idx = np.where(df_id.iloc[:,6] == 'arriving', True, False)
    driving_idx = np.where(df_id.iloc[:,6] == 'driving', True, False)
    billing_idx = np.where(df_id.iloc[:,6] == 'billing', True, False)
    done_idx = np.where((df_id.iloc[:,6] == 'done') | (df_id.iloc[:,6] == 'orderable_canceled') | (df_id.iloc[:,6] == 'closed'), True, False)

    approaching_time_vec = np.array(df_id.iloc[approaching_idx,2])
    arriving_time_vec = np.array(df_id.iloc[arriving_idx,2])
    driving_time_vec = np.array(df_id.iloc[driving_idx,2])
    billing_time_vec = np.array(df_id.iloc[billing_idx,2])
    done_time_vec = np.array(df_id.iloc[done_idx,2])

    done_flag_vec = np.array(df_id.iloc[done_idx,6])

    arriving_fetch_idx = 0
    driving_fetch_idx = 0
    billing_fetch_idx = 0
    id_idx = np.where(json_car_id_vec == car_id, True, False)
    id_time_vec = json_time_vec[id_idx]
    id_lat_vec = json_lat_vec[id_idx]
    id_lng_vec = json_lng_vec[id_idx]
    id_timestamp_vec = json_timestamp_vec[id_idx]

    not_aircle_vec = np.array([False]*len(id_time_vec))
    for i in range(0, len(done_flag_vec)):

        if done_flag_vec[i] == 'done':
            approaching_time = approaching_time_vec[i]
            arriving_time = arriving_time_vec[arriving_fetch_idx]
            arriving_fetch_idx += 1
            driving_time = driving_time_vec[driving_fetch_idx]
            driving_fetch_idx += 1
            billing_time = billing_time_vec[billing_fetch_idx]
            billing_fetch_idx += 1
            done_time = done_time_vec[i]

            time_diff = np.array([compare_time_string(approaching_time, id_time) for id_time in id_time_vec])
            min_val = np.min(time_diff)
            approaching_time_idx = np.where(time_diff == min_val, True, False)

            time_diff = np.array([compare_time_string(arriving_time, id_time) for id_time in id_time_vec])
            min_val = np.min(time_diff)
            arriving_time_idx = np.where(time_diff == min_val, True, False)

            time_diff = np.array([compare_time_string(driving_time, id_time) for id_time in id_time_vec])
            min_val = np.min(time_diff)
            driving_time_idx = np.where(time_diff == min_val, True, False)

            time_diff = np.array([compare_time_string(billing_time, id_time) for id_time in id_time_vec])
            min_val = np.min(time_diff)
            billing_time_idx = np.where(time_diff == min_val, True, False)

            time_diff = np.array([compare_time_string(done_time, id_time) for id_time in id_time_vec])
            min_val = np.min(time_diff)
            done_time_idx = np.where(time_diff == min_val, True, False)

            cumsum_idx = np.cumsum(approaching_time_idx) + np.cumsum(done_time_idx)
            time_interval = np.where((0 < cumsum_idx) & (cumsum_idx <= np.sum(approaching_time_idx)), True, False)

            cumsum_idx = np.cumsum(approaching_time_idx) + np.cumsum(arriving_time_idx)
            approaching_interval = np.where((0 < cumsum_idx) & (cumsum_idx <= np.sum(approaching_time_idx)), True, False)

            cumsum_idx = np.cumsum(arriving_time_idx) + np.cumsum(driving_time_idx)
            arriving_interval = np.where((0 < cumsum_idx) & (cumsum_idx <= np.sum(arriving_time_idx)), True, False)

            cumsum_idx = np.cumsum(driving_time_idx) + np.cumsum(billing_time_idx)
            driving_interval = np.where((0 < cumsum_idx) & (cumsum_idx <= np.sum(driving_time_idx)), True, False)

            cumsum_idx = np.cumsum(billing_time_idx) + np.cumsum(done_time_idx)
            billing_interval = np.where((0 < cumsum_idx) & (cumsum_idx <= np.sum(billing_time_idx)), True, False)

            state_vec = np.array(["approaching"]*len(time_interval))
            state_vec[time_interval] = "done"
            state_vec[approaching_interval] = "approaching"
            state_vec[arriving_interval] = "arriving"
            state_vec[driving_interval] = "driving"
            state_vec[billing_interval] = "billing"
            state_vec = state_vec[time_interval]

            not_aircle_vec = not_aircle_vec | ~time_interval

            center_lat = np.mean(np.array(id_lat_vec)[time_interval])
            center_lng = np.mean(np.array(id_lng_vec)[time_interval])
            m = folium.Map(location=[center_lat, center_lng], zoom_start=13)

            lat_vec = np.array(id_lat_vec)[time_interval]
            lng_vec = np.array(id_lng_vec)[time_interval]
            timestamp_vec = np.array(id_timestamp_vec)[time_interval]

            for j in range(0, len(lat_vec)-1):
                if j == 0:
                    folium.Marker(location=[lat_vec[j], lng_vec[j]], icon=folium.Icon(color="green")).add_to(m)
                elif j == len(lat_vec)-2:
                    folium.Marker(location=[lat_vec[j+1], lng_vec[j+1]], icon=folium.Icon(color="red")).add_to(m)

                # pdb.set_trace()
                # html_color = '#%02X%02X%02X' % (int(color_vec[0]), int(color_vec[1]), int(color_vec[2]))

                # folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color=cplt(j)).add_to(m)
                if state_vec[j] == "approaching":
                    folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="green", popup=j).add_to(m)
                elif state_vec[j] == "arriving":
                    folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="brown", popup=j).add_to(m)
                elif state_vec[j] == "driving":
                    folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="blue", popup=j).add_to(m)
                elif state_vec[j] == "billing":
                    folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="purple", popup=j).add_to(m)
                else:
                    folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="black", popup=j).add_to(m)

            m.save('aircle_' + date_string + '_' + str(int(car_id)) + '_' + str(i) + '.html')
            df_result = pd.DataFrame({'lat': lat_vec, 'lng': lng_vec, 'timestamp': timestamp_vec, 'state': state_vec})
            with open('aircle_' + date_string + '_' + str(int(car_id)) + '_' + str(i) + '.pickle', 'wb') as f:
                pickle.dump(df_result , f)

    lat_vec = np.array(id_lat_vec)[not_aircle_vec]
    lng_vec = np.array(id_lng_vec)[not_aircle_vec]
    timestamp_vec = np.array(id_timestamp_vec)[not_aircle_vec]
    df_residual = pd.DataFrame({'lat': lat_vec, 'lng': lng_vec, 'timestamp': timestamp_vec})
    with open('residual_' + date_string + '_' + str(int(car_id)) + '.pickle', 'wb') as f:
        pickle.dump(df_residual , f)
