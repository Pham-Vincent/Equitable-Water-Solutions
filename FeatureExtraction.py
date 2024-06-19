import numpy as np
import pandas as pd
from datetime import datetime
from scipy.interpolate import interp1d



def interpolation(DataFrame):


  DataFrame['Salinity'] = DataFrame['Salinity'].interpolate(method='linear')
  print(DataFrame)
  return DataFrame



#The purpose of this function is to calculate the average salinity values for each day, using hourly data recorded throughout the day.
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
    
  print(NewDates)
  #Date.columns=['Time','Salinity']
  
  
  
  return interpolation(NewDates)




  
 




