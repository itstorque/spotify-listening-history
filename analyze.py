import os

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sb

data_folder = "MyData/"

df = None
COLS = ['ts', 'username', 'platform', 'ms_played', 'conn_country', 'ip_addr_decrypted', 'user_agent_decrypted', 'master_metadata_track_name', 'master_metadata_album_artist_name', 'master_metadata_album_album_name', 'spotify_track_uri', 'episode_name', 'episode_show_name', 'spotify_episode_uri', 'reason_start', 'reason_end', 'shuffle', 'skipped', 'offline', 'offline_timestamp', 'incognito_mode']

def show_top_entries(df, cols=['master_metadata_album_artist_name', 'master_metadata_track_name', 'master_metadata_album_album_name', 'ms_played'], count=30):
    print(df[cols].head(count))

def time_listened_to(df, units="h"):
    units = units[0].lower()
    
    time = df["ms_played"].sum() / 1000 # in seconds
    
    if units == "s":
        return time
    elif units == "m":
        return time / 60
    elif units == "h":
        return time / 3600
    elif units == "d":
        return time / 3600 / 24

def track_listen_time_by_artist(df, artist, sorted=True, keep=['master_metadata_album_artist_name', 'master_metadata_album_album_name']):
    
    aggregation_functions = {'ms_played': 'sum', 'master_metadata_track_name': 'first'}
    
    for i in keep:
        aggregation_functions[i] = 'first'
        
    filtered = filter_by_artist(df, artist_name=artist)
        
    res = filtered.groupby(filtered['master_metadata_track_name']).aggregate(aggregation_functions)
    
    if sorted:
        return sorted_by_listen_time(res)
    else:
        return res
    
def sorted_by_listen_time(df):
    return df.sort_values(by=['ms_played'], ascending=False)

def time_listened_to_artist(df, artist_name, units="h"):
    filtered = filter_by_artist(df, artist_name)
    return time_listened_to(filtered, units=units)

def filter_by_artist(df, artist_name):
    return df.loc[df['master_metadata_album_artist_name'] == artist_name]

for file in os.listdir(data_folder):
    
    if file[-5:]==".json":
        temp = pd.read_json(data_folder + file)
        
        if df is None:
            print("AVAILABLE COLS", temp.columns.values.tolist())
            df = temp
        else:
            pd.concat([df, temp])
            
print(df[COLS])

K = df.sort_values(by=['ms_played'], ascending=False)
show_top_entries(K)

HS = df.loc[df['master_metadata_album_artist_name'] == "Harry Styles"]

show_top_entries(  HS  )

print(time_listened_to_artist(df, "Harry Styles", "hours"))
print(time_listened_to_artist(df, "dodie", "hours"))
print(time_listened_to_artist(df, "girl in red", "hours"))

print(track_listen_time_by_artist(df, "Harry Styles"))

# sb.relplot(df, x="master_metadata_album_artist_name", y="ms_played")
plt.show()