import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json
import glob
import pickle

import datetime

import folium

import pdb

def calc_window_mean_mat(lat_lng_df, window_size):

    lat_vec = np.array(lat_lng_df.iloc[:,0])
    lng_vec = np.array(lat_lng_df.iloc[:,1])
    lat_diff = lat_vec[1:len(lat_vec)] - lat_vec[0:(len(lat_vec)-1)]
    lng_diff = lng_vec[1:len(lng_vec)] - lng_vec[0:(len(lng_vec)-1)]

    window_mean_mat = np.array([[0.0]*2 for i in range(0, len(lat_diff))])
    for i in range(0, (len(window_mean_mat)-window_size)):
        mean_lat = np.mean(lat_diff[i:(i+window_size)])
        mean_lng = np.mean(lng_diff[i:(i+window_size)])
        window_mean_mat[int(i+window_size/2)] = [mean_lat, mean_lng]

    return window_mean_mat

def mask_transition_part(zero_idx_vec, threshold_len, window_size):
    cumsum_vec = np.cumsum(zero_idx_vec)
    mask_vec = np.array([False]*len(cumsum_vec))
    baseline = 0
    hit_len = 0
    mask_flag = False

    for i in range(int(window_size/2), len(cumsum_vec)-int(window_size/2)):
        if zero_idx_vec[i]:
            hit_len += 1
            delta = cumsum_vec[i] - baseline
            if threshold_len < delta:
                mask_flag = True

        else:
            if 0 < hit_len:
                mask_vec[(i-hit_len):i] = mask_flag
            baseline = cumsum_vec[i]
            hit_len = 0
            mask_flag = False

    return mask_vec

def separate_df(df):
    lat_vec = np.array(df.iloc[:,0])
    lng_vec = np.array(df.iloc[:,1])
    timestamp_vec = np.array(df.iloc[:, 2])

    diff_lat = lat_vec[1:len(lat_vec)] - lat_vec[0:(len(lat_vec)-1)]
    diff_lng = lng_vec[1:len(lng_vec)] - lng_vec[0:(len(lng_vec)-1)]
    diff_timestamp = timestamp_vec[1:len(timestamp_vec)] - timestamp_vec[0:(len(timestamp_vec)-1)]

    v_vec = np.sqrt(diff_lat**2 + diff_lng**2)*100000/diff_timestamp

    sep_count = 0
    start_pos = 0
    df_dict = {}
    for i in range(0, len(v_vec)):
        if 100 < v_vec[i]:
            df_dict[sep_count] = df.iloc[start_pos:i,:]
            start_pos = i
            sep_count += 1
    df_dict[sep_count] = df.iloc[start_pos:len(df),:]

    return df_dict

files = glob.glob('./pickle_residual/*')
files = np.sort(files)

for file in files:
    with open(file, 'rb') as f:
        df_total = pickle.load(f)

    if len(df_total) == 0:
        continue

    df_dict = separate_df(df_total)

    print("*** " + file + " ***")
    tmp = file.split('/')[2]
    date_string = tmp.split('_')[1]
    tmp = tmp.split('_')[2]
    car_id = tmp.split('.')[0]
    
    for key in df_dict.keys():
        df = df_dict[key]

        lat_vec = np.array(df.iloc[:,0])
        lng_vec = np.array(df.iloc[:,1])
        time_vec = np.array(df.iloc[:,2])

        window_mean_mat = calc_window_mean_mat(df, 12)
        if(len(window_mean_mat) == 0):
            continue

        if (file == "./pickle_residual/residual_2020-07-08_131.pickle") & (key == 3):
            pdb.set_trace()
        v_vec = np.sqrt(window_mean_mat[:,0]**2 + window_mean_mat[:,1]**2)*100000/5

        zero_idx_vec = np.where(v_vec < 2.5, True, False)
        mask_vec = mask_transition_part(zero_idx_vec, 18, 12)

        # pdb.set_trace()

        center_lat = np.mean(np.array(lat_vec))
        center_lng = np.mean(np.array(lng_vec))
        m = folium.Map(location=[center_lat, center_lng], zoom_start=13)
        for j in range(0, len(df)-1):
            if j == 0:
                folium.Marker(location=[lat_vec[j], lng_vec[j]], icon=folium.Icon(color="green")).add_to(m)
            elif j == len(lat_vec)-2:
                folium.Marker(location=[lat_vec[j+1], lng_vec[j+1]], icon=folium.Icon(color="red")).add_to(m)

            # pdb.set_trace()
            # html_color = '#%02X%02X%02X' % (int(color_vec[0]), int(color_vec[1]), int(color_vec[2]))

            # folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color=cplt(j)).add_to(m)
            if mask_vec[j]:
                folium.Marker(location=[lat_vec[j], lng_vec[j]], icon=folium.Icon(color="blue")).add_to(m)
                folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="blue", popup=j).add_to(m)
            else:
                folium.PolyLine(locations=[[lat_vec[j], lng_vec[j]], [lat_vec[j+1], lng_vec[j+1]]], color="black", popup=j).add_to(m)

        m.save('estimate_residual_' + date_string + '_' + car_id + '_' + str(key) + '.html')

        fig = plt.figure()
        plt.plot(mask_vec*5)
        plt.plot(v_vec)
        fig.savefig('v_mask_residual_' + date_string + '_' + car_id + '_' + str(key) + '.png')
        plt.close()
