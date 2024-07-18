import pandas as pd 
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
import numpy as np

def AverageDailySalinity(DataFrame):

  #Reformats The Time So We can filter by months
  DataFrame['Time'] = DataFrame['Time'].dt.strftime('%m')
  DataFrame = DataFrame.drop(columns=['PermitNumber'])
  DataFrame=DataFrame.drop(8771)
  grouped_df = DataFrame.groupby('Time').mean().reset_index()
  return(grouped_df)

  

config = {'displaylogo': False,}
df = pd.read_csv('static\csv\AA2003S009(05) (1).csv')
df['Time'] = pd.to_datetime(df['Time'])
df=AverageDailySalinity(df)

fig = go.Figure()

depths = [30, 25, 20, 15, 10, 5, 0] 
ColorForGraph=['#030582','#0f1180','#1d1f80','#474b96','#5b60b0','#7377bd','#9597c2']
# Add bar traces for each depth
for depth,color in zip(depths,ColorForGraph):
  fig.add_trace(go.Scatter(x=df['Time'], y=df['Depth:'+str(depth)], name='Depth:'+str(depth),fill='tozeroy',mode='lines',fillcolor='rgba(0, 100, 80, 0.2)'))

# Update layout
fig.update_layout(
    title='Salinity Depth Measurements Over Time',
    xaxis_title='Time',
    yaxis_title='Salinity',
    barmode='overlay',  # Group bars for each depth at each time
    legend_title='Depth',
)
fig.update_traces(hovertemplate='Salinity Level:%{y}')


# Show the plot
fig.show()
  