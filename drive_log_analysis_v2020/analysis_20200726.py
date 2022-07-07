import sys

import json
import glob

import pdb

file_format = sys.argv[1]
files = glob.glob(file_format + '*.json')
car_id_vec = []
for file in files:
    with open(file) as f:
        df = json.load(f)

    items = df['Items']

    for item in items:
        car_id_vec.append(item['car_id'])

print(len(set(car_id_vec)))
