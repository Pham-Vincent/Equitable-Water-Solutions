""" 
Title: Geocode.py
Author: Vincent Pham

Functionality: This Python script will look at multiple rows and display any discrepencies between them. I am using this to check the longitude and latitude. I am checking if the longitude and Latitude given are the same/similar to the ones I get.

Output: Displays the row in which discrepency occurs
Last Edited: 4/22/2024
 """

import pandas as pd
import numpy as np

def main():
  
  Discrepency_df = pd.read_csv('Maryland_Tidal_Locations Coordinate Comparison.csv')
  Discrepency_df=Discrepency_df[["Fixed Longitudes","Fixed Latitudes","Longitude","Latitude"]]

  #Creates Adds 2 columns to find the discrepency of Longitude and Latitude
  Discrepency_df['discrepancyLongitude'] = ' '
  Discrepency_df['discrepancyLatitude'] = ' '

  #Iterates throught the entire Columns of Longitude and Latitude
  for i in range(len(Discrepency_df)):
    #Gets the Values of my Geoencoded Longitude and Latitude
    Longitude = Discrepency_df.loc[i,"Longitude"]
    Latitude = Discrepency_df.loc[i,"Latitude"]
    #Gets Values From their Geoencoded Longitude and Latitude
    FixedLongitude = Discrepency_df.loc[i,"Fixed Longitudes"]
    FixedLatitude = Discrepency_df.loc[i,"Fixed Latitudes"]
    
    #Compares and sees if there is any different 
    discrepancyLongitude = abs(Longitude - FixedLongitude)
    discrepancyLatitude = abs(Latitude - FixedLatitude)

    #Adds The Dicrepency Values Rounded to the 4th decimal Place
    Discrepency_df.loc[i, 'discrepancyLongitude'] = discrepancyLongitude.round(decimals=4)
    Discrepency_df.loc[i, 'discrepancyLatitude'] = discrepancyLatitude.round(decimals=4)


    #Commented Out but displays Any Discrepency Higher than 1 
    """ if(abs(FixedLatitude - Latitude) > 1):
      print("Check Row " + str(i) +" Discrepecy is: "+ str(FixedLatitude - Latitude) +" For Latitude")
    elif(abs(FixedLongitude - Longitude) > 1):
      print("Check Row " + str(i) +" Discrepecy is: "+ str(FixedLongitude - Longitude) +" For Longitude") """

  
  #Creates a CSV of the Discrepency Longitude and Latitude
  Discrepency_df[['discrepancyLongitude','discrepancyLatitude']].to_csv('Discrepency.csv',index=False)  
    
    


      
if __name__ == '__main__':
  main()
