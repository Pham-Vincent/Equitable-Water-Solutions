""" 
Title: Geocode.py
Author: Vincent Pham

Functionality: This Python script will look at multiple rows and display any discrepencies between them. I am using this to check the longitude and latitude. I am checking if the longitude and Latitude given are the same/similar to the ones I get.

Output: Displays the row in which discrepency occurs
Last Edited: 4/4/2024
 """

import pandas as pd
import numpy as np

def main():
  Discrepency_df = pd.read_csv('Maryland_Tidal_Locations_ShortList.csv')
  Discrepency_df=Discrepency_df[["Fixed Longitudes","Fixed Latitudes","Longitude","Latitude"]]
  
  for i in range(len(Discrepency_df)):
    Longitude = Discrepency_df.loc[i,"Longitude"]
    Latitude = Discrepency_df.loc[i,"Latitude"]
    FixedLongitude = Discrepency_df.loc[i,"Fixed Longitudes"]
    FixedLatitude = Discrepency_df.loc[i,"Fixed Latitudes"]

    if(abs(FixedLatitude - Latitude) > 1):
      print("Check Row " + str(i) +" Discrepecy is: "+ str(FixedLatitude - Latitude) +" For Latitude")
    elif(abs(FixedLongitude - Longitude) > 1):
      print("Check Row " + str(i) +" Discrepecy is: "+ str(FixedLongitude - Longitude) +" For Longitude")



      
if __name__ == '__main__':
  main()
