import googlemaps
import os
import pandas as pd
import numpy as np
def main():

#
# API_KEY =

  map_client = googlemaps.Client(API_KEY)
  Address_data = pd.read_csv('Equitable-Water-Solutions\Geocode Script\(imp)MD_Surface Water Permits 12JUL2021.csv')
  
  Address_data =Address_data.head(894)
  
  Data_df = Address_data[['Location']]
  GeoLocation = pd.DataFrame()


  
  
  """ for i in range(2,894):
    Address = Data_df.iloc[i]['Location']
   
    response = map_client.geocode(Address)
    if response: 
      Latitude = response[0]['geometry']['location']['lat']
      Longitude = response[0]['geometry']['location']['lng']
      GeoLocation.loc[i, 'Latitude'] = Latitude
      GeoLocation.loc[i, 'Longitude'] = Longitude
    else:
       GeoLocation.loc[i, 'Latitude'] = 'N/A'
       GeoLocation.loc[i, 'Longitude'] = 'N/A'
      
    GeoLocation.to_csv('GeoLocation.csv',index=False) """

    
if __name__ == '__main__':
  main()


