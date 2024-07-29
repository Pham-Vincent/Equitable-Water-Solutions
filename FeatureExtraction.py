""" 
Title: FeatureExtraction
Author: Vincent Pham

Functionality: This file facilitates the extraction of data from time series, enhancing its readability and usability.

Output: Database Connection
Date:6/21/2024
"""


import numpy as np
import pandas as pd
from datetime import datetime
from scipy.interpolate import interp1d


#This Function Is Used to Get Missing Data Hourly Between Points
def interpolation(DataFrame):

  DataFrame['Salinity'] = DataFrame['Salinity'].interpolate(method='linear')

  return DataFrame



#The purpose of this function is to calculate the average salinity values for each day, using hourly data recorded throughout the day Making the Graph More Readable.
def AverageDailySalinity(DataFrame):

  Date = pd.DataFrame(columns=['Date_Reformatted'])

  NewDates=pd.DataFrame(columns=['Time'])

  NewDates['Time'] = DataFrame['Time']
  #Reformats The Time So There is no Hours/Minutes/Seconds
  Date['Date_Reformatted'] = DataFrame['Time'].dt.strftime('%Y-%m-%d')

  #Remove All the Duplicate Dates
  Date=pd.DataFrame(Date['Date_Reformatted'].unique())

  #Gives The DataFrame Column a Name
  Date.columns=['Date_Reformatted']

  #Change Column to Datatype Datetime
  Date['Date_Reformatted'] = pd.to_datetime(Date['Date_Reformatted'])

  #Iterates Through Dates and Then Gets Average Salinity For Each Day  
  for i in range(len(Date)):
    CurrentDate = Date.loc[i,"Date_Reformatted"]
    
    #Gets all Salinity Values That are in a Certain Date 
    filtered_df = DataFrame[DataFrame['Time'].dt.date == CurrentDate.date()]

    #Converts Salinity DF to List With Float Variables
    Salinity_List = filtered_df['Salinity'].astype(float).values.tolist()

    CurrentDate = pd.to_datetime(CurrentDate, format='%Y-%m-%d')  
    
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Salinity'] = np.mean(Salinity_List)     
  
  return interpolation(NewDates)

# Get the monthly averages for salinity at each depth
def MonthlyAverages(DataFrame):

  #Reformats The Time So We can filter by months
  DataFrame['Time'] = DataFrame['Time'].dt.strftime('%b')
  #Extra Data For 2023 only want 2022
  DataFrame=DataFrame.drop(8760)
  #Groups The Data my Month and Gets the Average
  grouped_df = DataFrame.groupby('Time',as_index=False).mean().reset_index()
  return(grouped_df)




  
 




