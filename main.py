import json
import os
import gmplot
import numpy as np
import pandas as pd
import datetime

lpath = os.getcwd()
rpath =r"\\Takeout\takeout-20170501T190823Z-001\Takeout\Location History"

path=lpath+rpath
print "files in the directory:", os.listdir(path)

#load json file
with open(os.path.join(path,"LocationHistory.json")) as jf:
	f = json.load(jf)

#build the pandas dataframe
df = pd.DataFrame.from_dict(f['locations'], orient='columns')
#select the columns desired and rename them
df=df[['accuracy','altitude','latitudeE7','longitudeE7','timestampMs','velocity']]
df.rename(columns={'latitudeE7':'lat','longitudeE7':'long'}, inplace=True)
#add field with format datestamp
df['datestamp'] = df['timestampMs'].apply(lambda x: datetime.datetime.fromtimestamp(
        int(x)/1000
    ).strftime('%Y-%m-%d'))
print list(df)
print len(df)

#df_reduced = df[(df['accuracy']<50) & (df['velocity']>0)]
df_reduced = df[(df['datestamp']>='2017-05-01') & (df['datestamp']<='2017-05-05')]
print len(df_reduced)

#define map for central London
gmap_scat = gmplot.GoogleMapPlotter(51.511158, -0.136686,12)
#gmap_scat.scatter(df_reduced['lat'], df_reduced['long'], '#3B0B39', size=15, marker=False)
gmap_scat.plot(df_reduced['lat'], df_reduced['long'], 'cornflowerblue', edge_width=10)
gmap_scat.draw("mymap.html")

gmap_heat = gmplot.GoogleMapPlotter(51.511158, -0.136686,12)
gmap_heat.heatmap(df_reduced['lat'], df_reduced['long'])
#gmap.plot(df['lats'], df['longs'], 'cornflowerblue', edge_width=10)
gmap_heat.draw("mymap_heat.html")


