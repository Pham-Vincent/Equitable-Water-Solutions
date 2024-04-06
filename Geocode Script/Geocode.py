

""" 
Title: Geocode.py
Author: Vincent Pham

Functionality: This Python program utilizes the google maps API Key to geoencode the Addresses -> Latitude and Longitude. This Program will take a csv file and turn it into a Dataframe. After this program will make an Google maps API call to geoencode the code and insert those values into a dataframe. After it has geoencoded all the addresses it will create a csv file with all the new Longitude and Latitude data

Output: CSV file
Last Edited: 4/4/2024
 """

#Imported Libraries 
import googlemaps
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
def main():
  
  #Loads Information from env and runs code
  load_dotenv()
  API_KEY= os.environ.get('MAP_KEY')

 
  #Loads the Google Maps Api by Checking API key
  map_client = googlemaps.Client(API_KEY)

#Turns the csv into dataframe and gets the first 894
  Data_df = pd.read_csv('(imp)MD_Surface Water Permits 12JUL2021.csv')
  Data_df = Data_df.head(895)

#Creates a Dataframe of only the Locations and creates and empty dataframe to input longitude and latitude
  Address_df = Data_df[['Location']]
  GeoLocation = pd.DataFrame()


  
  #Will iterate through the entire dataframe and turn Address -> Longitude and Latitude
  for i in range(len(Data_df)):
    #Gets Address From dataframe
    Address = Address_df.iloc[i]['Location']
    #Api Call and turns Address -> Coordinates
    response = map_client.geocode(Address)

    #If finds Coordinates Will insert into Geolocation DataFrame and if not found will input N/A
    if response: 
      Latitude = response[0]['geometry']['location']['lat']
      Longitude = response[0]['geometry']['location']['lng']
      GeoLocation.loc[i, 'Latitude'] = Latitude
      GeoLocation.loc[i, 'Longitude'] = Longitude
    else:
       GeoLocation.loc[i, 'Latitude'] = 'N/A'
       GeoLocation.loc[i, 'Longitude'] = 'N/A'
      
    #Turns into csv 
    GeoLocation.to_csv('GeoLocation.csv',index=False)  

    
if __name__ == '__main__':
  main()


