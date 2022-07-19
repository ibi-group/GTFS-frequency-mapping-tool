import gtfs_functions as gtfs
import pandas as pd
import geopandas as gpd
import zipfile
import sys
import os
import shutil

#Utils
def compareOldandNew(old, new):
    a = new.merge(old, on = ['segment_id', 'window'], how = 'outer', indicator = True)
    a.drop(columns = ['s_st_id_y',
        's_st_name_y', 'day_type_y'], inplace = True)
    a.columns = a.columns.str.replace('_x', '')
    a.columns = a.columns.str.replace('_y', '_old')
    a.loc[a["geometry"].isna(), "geometry"] = a.geometry_old
    a.drop(columns = ['geometry_old'], inplace = True)

    print(a.columns)

    a['total_freq_diff'] = round(a.trips_in_p - a.trips_in_p_old, 2)
    a['max_freq_diff'] = round(a.hourly_fre - a.hourly_fre_old, 2)
    a['headway_diff'] = round(a.headway_mi - a.headway_mi_old, 2)
    #clean up merge names
    a.rename(columns = {'_merge': 'seg_type'}, inplace = True)
    a.seg_type.replace({'both': 'both_feeds', 
    'left_only' : 'new_segment', 'right_only' : 'old_segment'}, inplace = True)
    a = gpd.GeoDataFrame(a, geometry = 'geometry')

    a['seg_type'] = a.seg_type.astype(object)

    return a

def readZipShapefile(name):
    if os.path.exists(name):
        shutil.rmtree(name)
    os.mkdir(name)
    with zipfile.ZipFile(name + ".zip","r") as zip_ref:
        zip_ref.extractall(name)

    df = gpd.read_file(name + "/" + name + ".shp")
    return df
    
#Main
old = readZipShapefile(sys.argv[1])
new = readZipShapefile(sys.argv[2])

old_vs_new = compareOldandNew(old, new)

if not os.path.exists('feed_comparison'): 
  os.makedirs('feed_comparison')

old_vs_new.to_file('feed_comparison/feed_comparison.shp')