import pandas as pd
from geopy import distance
from geopy.distance import vincenty

bike_loc = "Capital_Bike_Share_Locations.csv"
df_bike_loc = pd.read_csv(bike_loc)
df_bike_loc = df_bike_loc.drop(
    ["OBJECTID", "ID", "TERMINAL_NUMBER", "INSTALLED", "LOCKED", "INSTALL_DATE", "REMOVAL_DATE", "TEMPORARY_INSTALL",
     "NUMBER_OF_BIKES", "NUMBER_OF_EMPTY_DOCKS", "SE_ANNO_CAD_DATA", "OWNER", "X", "Y"], axis=1)

metro_loc = "Metro Stops.csv"
df_metro_loc = pd.read_csv(metro_loc)


def get_coord(address):
    coords = df_bike_loc[df_bike_loc['ADDRESS'].str.match(address)]
    print(coords)
    lat = coords.iloc[0]["LATITUDE"]
    long = coords.iloc[0]["LONGITUDE"]
    result = [lat, long]
    print(result)
    return result


def compare_points():
    distance.vincenty()
    in_range = []
    for bike_point, row in df_bike_loc.iterrows():
        for metro_point, srow in df_metro_loc.iterrows():
            bike = (row["LATITUDE"], row["LONGITUDE"])
            metro = (srow["Lat"], srow["Lon"])
            try:
                miles = vincenty(bike, metro).miles
                print(miles)
                if miles < 1.0:
                    in_range.append(True)
                else:
                    in_range.append(False)
            except ValueError as e:
                print("Unforomatted Data")
                in_range.append(False)
    print(in_range)
    length = len(df_bike_loc)
    df_bike_loc["IN_RANGE"] = in_range[:length]
    print(df_bike_loc)
    print(df_bike_loc.groupby(["IN_RANGE"]).sum())

compare_points()
# get_coord("New Hampshire Ave & T St NW")
