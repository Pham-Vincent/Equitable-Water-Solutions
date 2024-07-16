import pandas as pd 
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
from scipy.interpolate import interp1d
import numpy as np

def AverageDailySalinity(DataFrame):

  Date = pd.DataFrame(columns=['Date_Reformatted'])

  NewDates=pd.DataFrame(columns=['Time'])

  NewDates['Time'] = DataFrame['Time']
  #Reformats The Time So There is no Hours/Minutes/Seconds
  Date['Date_Reformatted'] = DataFrame['Time'].dt.strftime('%m')
  #Remove All the Duplicate Dates
  #Date=pd.DataFrame(Date['Date_Reformatted'].unique())

  #Gives The DataFrame Column a Name
  Date.columns=['Date_Reformatted']

  #Change Column to Datatype Datetime
  #Date['Date_Reformatted'] = pd.to_datetime(Date['Date_Reformatted'])
  #print(['Date_Reformatted'])
   #Iterates Through Dates and Then Gets Average Salinity For Each Day  
  for i in enumerate(0,12):
    #Gets all Salinity Values That are in a Certain Date 
    filtered_df = DataFrame[DataFrame['Time'].dt.date == CurrentDate.date()]

    #Converts Salinity DF to List With Float Variables
    Depth0 = filtered_df['Depth:0'].astype(float).values.tolist()
    Depth15 = filtered_df['Depth:15'].astype(float).values.tolist()
    Depth30 = filtered_df['Depth:30'].astype(float).values.tolist()

    CurrentDate = pd.to_datetime(CurrentDate, format='%Y-%m-%d')  
    
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:0'] = np.mean(Depth0)     
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:15'] = np.mean(Depth15)     
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:30'] = np.mean(Depth30)     
    print(NewDates)
  return interpolation(NewDates)
"""
def interpolation(DataFrame):

  DataFrame['Depth:0'] = DataFrame['Depth:0'].interpolate(method='linear')
  DataFrame['Depth:15'] = DataFrame['Depth:15'].interpolate(method='linear')
  DataFrame['Depth:30'] = DataFrame['Depth:30'].interpolate(method='linear')

  return DataFrame

config = {'displaylogo': False,}
df = pd.read_csv('static\csv\AA2003S009(05) (1).csv')
df = df[['PermitNumber','Time','Depth:0','Depth:15','Depth:30']]
df['Time'] = pd.to_datetime(df['Time'])
df=AverageDailySalinity(df)
""" 
SalinityPlotted = go.Figure()

SalinityPlotted.add_trace(go.Bar(
    x=df['Time'],
    y=df['Depth:0'],
    mode='lines',  # Include markers for better visibility of colors
    hovertemplate='Time: %{x}<br>Salinity: %{y}',
    name="Depth 0"
))

# Add trace for Depth 15
SalinityPlotted.add_trace(go.Bar(
    x=df['Time'],
    y=df['Depth:15'],
    mode='lines',  # Include markers for better visibility of colors
    hovertemplate='Time: %{x}<br>Salinity: %{y}',
    name="Depth 15"
))

# Add trace for Depth 30
SalinityPlotted.add_trace(go.Bar(
    x=df['Time'],
    y=df['Depth:30'],
    mode='lines',  # Include markers for better visibility of colors
    hovertemplate='Time: %{x}<br>Salinity: %{y}',
    name="Depth 30"
))

# Customize layout
SalinityPlotted.update_layout(
    width=700,
    height=550,
    title="Calvert Cliffs Nuclear Power Plant Salinity Levels",
    xaxis=dict(title="Time"),
    yaxis=dict(title="Salinity Levels"),
    showlegend=True  # Set to True to show legend with trace names
)
SalinityPlotted.show()




 """