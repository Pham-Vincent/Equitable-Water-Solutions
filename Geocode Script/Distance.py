""" 
Title: Distance.py
Author: Vincent Pham

Functionality: This Python script will look at The Coordinates Given and The coordinates I have Geoencoded and will find the distance between them 

Output: Creates a CSV that will contain the Distance
Last Edited: 4/23/2024
 """

import pandas as pd
import numpy as np 
from geopy.distance import geodesic
Distance_df = pd.read_csv('Maryland_Tidal_Locations Coordinate Comparison.csv')
Distance_df=Distance_df[["Fixed Longitudes","Fixed Latitudes","Longitude","Latitude"]]

#Creates Adds A column for distance
Distance_df['distance(km)'] = ' '
Distance_df['distance(meters)'] = ' '
Distance_df['distance(miles)'] = ' '

#Iterates throught the entire Columns of Longitude and Latitude
for i in range(len(Distance_df)):
  #Gets the Values of my Geoencoded Longitude and Latitude
  Longitude = Distance_df.loc[i,"Longitude"]
  Latitude = Distance_df.loc[i,"Latitude"]
  #Gets Values From their Geoencoded Longitude and Latitude
  FixedLongitude = Distance_df.loc[i,"Fixed Longitudes"]
  FixedLatitude = Distance_df.loc[i,"Fixed Latitudes"]

  #Make Sure it it (Latitude,Longitude)
  #Creates a Tuple to pass in geopy
  GivenAddress=(FixedLatitude,FixedLongitude)

  GeoencodedAddress=(Latitude,Longitude)

  Distance_df.loc[i, 'distance(km)'] = round(geodesic(GivenAddress,GeoencodedAddress).km,4)
  Distance_df.loc[i, 'distance(meters)'] = round(geodesic(GivenAddress,GeoencodedAddress).meters,4)
  Distance_df.loc[i, 'distance(miles)'] = round(geodesic(GivenAddress,GeoencodedAddress).miles,4)
  Distance_df[['distance(km)','distance(meters)','distance(miles)']].to_csv('Distance.csv',index=False)  
  
