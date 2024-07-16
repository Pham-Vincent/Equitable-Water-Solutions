import pandas as pd 
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
from scipy.interpolate import interp1d
import numpy as np

def AverageDailySalinity(DataFrame):

  #Reformats The Time So We can filter by months
  DataFrame['Time'] = DataFrame['Time'].dt.strftime('%m')
  DataFrame = DataFrame.drop(columns=['PermitNumber'])
  grouped_df = DataFrame.groupby('Time').mean().reset_index()
  return(grouped_df)

  

config = {'displaylogo': False,}
df = pd.read_csv('static\csv\AA2003S009(05) (1).csv')
df = df[['PermitNumber','Time','Depth:0','Depth:15','Depth:30']]
df['Time'] = pd.to_datetime(df['Time'])
df=AverageDailySalinity(df)

fig = go.Figure()

# Add bar traces for each depth
fig.add_trace(go.Bar(x=df['Time'], y=df['Depth:30'], name='Depth:30'))
fig.add_trace(go.Bar(x=df['Time'], y=df['Depth:15'], name='Depth:15'))
fig.add_trace(go.Bar(x=df['Time'], y=df['Depth:0'], name='Depth:0'))
# Update layout
fig.update_layout(
    title='Salinity Depth Measurements Over Time',
    xaxis_title='Time',
    yaxis_title='Salinity',
    barmode='overlay',  # Group bars for each depth at each time
    legend_title='Depth',
    template='plotly',
    

)

# Show the plot
fig.show()
