import numpy as np
import pandas as pd
import requests
from time import sleep
from datetime import datetime

headers = {'api_key': 'a6eec6a895a841429bf8d86bdab46295'}

def get_stations(LineCode=''):
    sleep(0.2)
    url = 'https://api.wmata.com/Rail.svc/json/jStations'
    params = {}
    if LineCode != '':
        params['LineCode'] = LineCode
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def get_bus_stops(Lat=0, Lon=0, Radius=0):
    sleep(0.2)
    url = 'https://api.wmata.com/Bus.svc/json/jStops'
    params = {}
    if Lat != 0:
        params['Lat'] = Lat
        params['Lon'] = Lon
        params['Radius'] = Radius
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def get_route_details(RouteID, Date=datetime.strftime(datetime.today(), '%Y-%m-%d'), IncludingVariations=False):
    sleep(0.2)
    url = 'https://api.wmata.com/Bus.svc/json/jRouteSchedule'
    params = {}
    params['RouteID'] = RouteID
    params['Date'] = Date
    params['IncludingVariations'] = IncludingVariations
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def get_stop_details(StopID, Date=datetime.strftime(datetime.today(), '%Y-%m-%d')):
    sleep(0.2)
    url = 'https://api.wmata.com/Bus.svc/json/jStopSchedule'
    params = {}
    params['StopID'] = StopID
    params['Date'] = Date
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None


yellow_stations = get_stations('YL')
blue_stations = get_stations('BL')

yellow_stations = pd.DataFrame(yellow_stations['Stations'])
blue_stations = pd.DataFrame(blue_stations['Stations'])

st_of_interest = {
   'YL': ['Braddock Road', 'King St-Old Town', 'Eisenhower Avenue', 'Huntington', 'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon', 'L\'Enfant Plaza'],
   'BL': ['Braddock Road', 'King St-Old Town', 'Van Dorn Street', 'Franconia-Springfield', 'Ronald Reagan Washington National Airport', 'Crystal City', 'Pentagon City', 'Pentagon', 'Arlington Cemetery', 'Rosslyn', 'L\'Enfant Plaza']
}

# st_of_interest = {
#     'YL': ['Braddock Road', 'King St-Old Town', 'Eisenhower Avenue', 'Huntington'],
#     'BL': ['Braddock Road', 'King St-Old Town', 'Van Dorn Street', 'Franconia-Springfield']
# }

stations = yellow_stations[yellow_stations['Name'].isin(st_of_interest['YL'])][['Name', 'Code', 'Lat', 'Lon']]
stations = stations.append(blue_stations[blue_stations['Name'].isin(st_of_interest['BL'])][['Name', 'Code', 'Lat', 'Lon']], ignore_index=True)
stations = stations.drop_duplicates(subset='Name')
stations = stations.set_index('Name')

stations.to_csv('data/metro_stations.csv')

stops = []
for station in stations.itertuples():
    for stop in get_bus_stops(
            getattr(station, 'Lat'),
            getattr(station, 'Lon'),
            100
            )['Stops']:
        stops.append(stop)
        stops[-1]['Nearest_Metro'] = getattr(station, 'Index')

stops = pd.DataFrame(stops)
stops2 = stops.drop(columns='Routes')

stops2.to_csv('data/bus_stops.csv', index=False)

routes = []
for i in stops['Routes']:
    routes.extend(i)
routes = list(pd.Series(routes).unique())

route_times = {'RouteID': [], 'Duration': [], 'StartLat': [], 'StartLon': [], 'EndLat': [], 'EndLon': []}
for route in routes:
    r = get_route_details(route, Date='2019-05-28')
    durations = []
    if r['Direction0'] != []:
        for trip in r['Direction0']:
            end_time = datetime.strptime(trip['EndTime'], '%Y-%m-%dT%H:%M:%S')
            start_time = datetime.strptime(trip['StartTime'], '%Y-%m-%dT%H:%M:%S')
            duration = end_time - start_time
            duration = duration.total_seconds()
            durations.append(duration)
        if r['Direction1'] != []:
            for trip in r['Direction1']:
                end_time = datetime.strptime(trip['EndTime'], '%Y-%m-%dT%H:%M:%S')
                start_time = datetime.strptime(trip['StartTime'], '%Y-%m-%dT%H:%M:%S')
                duration = end_time - start_time
                duration = duration.total_seconds()
                durations.append(duration)
        stop = get_stop_details(r['Direction0'][0]['StopTimes'][0]['StopID'])
        route_times['StartLat'].append(stop['Stop']['Lat'])
        route_times['StartLon'].append(stop['Stop']['Lon'])
        stop = get_stop_details(r['Direction0'][0]['StopTimes'][-1]['StopID'])
        route_times['EndLat'].append(stop['Stop']['Lat'])
        route_times['EndLon'].append(stop['Stop']['Lon'])
        route_times['RouteID'].append(route)
        route_times['Duration'].append(np.mean(durations))

pd.DataFrame(route_times).to_csv('data/bus_durations.csv', index=False)

