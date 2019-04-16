from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import pandas as pd
import numpy as np
import os
import json

session = Session(server_token="NyJghr9G5q4VEPkASLCEEQHrW2XEP9BvH_vxy6dd")
client = UberRidesClient(session)

MS = pd.read_csv("Metro Stops.csv")
MS

duration = []
for i in range(len(MS)):
    for j in range(len(MS)):
        if (i != j):
            response = client.get_price_estimates(
                start_latitude=MS['Lat'][i],
                start_longitude=MS['Lon'][i],
                end_latitude=MS['Lat'][j],
                end_longitude=MS['Lon'][j],
                seat_count=2
            )
            duration.append(response.json.get('prices'))

print(len(duration))
print(len(duration[0]))

columns = ['Start', 'End', 'product_name', 'distance', 'high_estimate',
           'low_estimate', 'duration']
index = range(len(duration)*len(duration[0]))
df_ = pd.DataFrame(index=index, columns=columns)

a = 0
for i in range(len(duration)):
    for j in range(len(duration[0])):
        print(duration[i][j]['display_name'])
        print(duration[i][j]['distance'])
        print(duration[i][j]['high_estimate'])
        print(duration[i][j]['low_estimate'])
        print(duration[i][j]['duration'])
        a += 1

print(a)

a = 0
b = 0
for i in range(len(duration)):
    if(b*9 > 107):
        b = 0
    for j in range(len(duration[0])):
        df_['Start'][a] = MS['Code'][np.floor(i/12)]
        if (np.floor(i/12) == 0):
            df_['End'][a] = MS['Code'][i % 12 + 1]
        else:
            df_['End'][a] = MS['Code'][b]
        df_['product_name'][a] = duration[i][j]['display_name']
        df_['distance'][a] = duration[i][j]['distance']
        df_['high_estimate'][a] = duration[i][j]['high_estimate']
        df_['low_estimate'][a] = duration[i][j]['low_estimate']
        df_['duration'][a] = duration[i][j]['duration']
        a += 1
        print(a, b)
    if(b == np.floor(i/12)-1):
        b += 2
    else:
        b += 1

df_.to_csv("Uber_Metro_data.csv", encoding='utf-8')

BS = pd.read_csv("Bus Stops.csv")
path = '/Users/binbinwu/Desktop/GW 2019 Spring Class/Hippo/Uber_2018_Q2'

datalist = []
filenames = []
for filename in os.listdir(path):
    # if (filename=="TeamSpellings.csv"):
    # df=pd.read_csv(path+'/'+filename,encoding = 'unicode_escape')
    # datalist.append(df)
    # filenames.append(filename)
    # i=i+1
    # else:
    df = pd.read_csv(path+'/'+filename)
    datalist.append(df)
    filenames.append(filename)
    # i=i+1

with open("washington_DC_censustracts.json", "r") as read_file:
    data = json.load(read_file)

maxid = datalist[7]['sourceid'].max()

for i in range(maxid):
    print(data['features'][i]['properties'])
