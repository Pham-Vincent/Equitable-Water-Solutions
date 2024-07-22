import pandas as pd 
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
import numpy as np


def AverageDailySalinity(DataFrame):

  #Reformats The Time So We can filter by months
  DataFrame['Time'] = DataFrame['Time'].dt.strftime('%b')
  DataFrame = DataFrame.drop(columns=['PermitNumber'])
  DataFrame=DataFrame.drop(8771)
  grouped_df = DataFrame.groupby('Time',as_index=False).mean().reset_index()
  return(grouped_df)

  
custom_colorscale = [
    [0.0, '#9597c2'],    # Lightest blue
    [0.2, '#5b60b0'],   # Lighter blue
    [0.4, '#474b96'],   # Light blue
    [0.6, '#1d1f80'],   # Dark blue
    [0.8, '#0f1180'],   # Blue
    [1.0, '#030582']   # Dark blue
]
config = {'displaylogo': False,}
df = pd.read_csv('static\csv\AA2003S009(05) (1).csv')
df['Time'] = pd.to_datetime(df['Time'])

df=AverageDailySalinity(df)
df = df[['Time', 'Depth:0', 'Depth:5', 'Depth:10', 'Depth:15', 'Depth:20', 'Depth:25', 'Depth:30']]
print(df)
df = df.transpose()

df = df[[4,3,7,0,8,6,5,1,11,10,9,2]]

new_index = df.iloc[0]
df = df[1:]
df.index=[0,5,10,15,20,25,30]
df.columns = new_index
fig = px.imshow(df, color_continuous_scale=custom_colorscale, aspect="auto")
fig.update_layout(
    yaxis_title='Depth',
    coloraxis_colorbar=dict(
        title='(dnɐsuoɥꞱ ɹǝԀ sʇɹɐԀ) ꞱԀԀ',  # Title for the color bar
        title_side='right'                   # Position the title at the top
    )
)

fig.update_traces(
    hovertemplate='<br>Month: %{x}<br>Depth: %{y}<br>Salinity: %{z}<extra></extra>',

)

fig.show()


""" 
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
   """