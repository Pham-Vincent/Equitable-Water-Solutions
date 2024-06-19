
import matplotlib.pyplot as plt
import numpy as np
import io
import os
import base64 
import pandas as pd
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
from flask import jsonify



def Maryland_Tidal_Graph(marker_title,Salinity_df):

  #Interacts with ModeBar
  config = {'displaylogo': False,}

  #creates The colorscale for Graph Currently Blue -> Red 
  color_scale = px.colors.diverging.Portland

  SalinityPlotted = go.Figure(
    data=go.Scatter(
        x=Salinity_df['Time'],
        y=Salinity_df['Salinity'],
        mode='lines+markers',  # Include markers for better visibility of colors
        marker=dict(
            color=Salinity_df['Salinity'],  # Map category data to color
            colorscale=color_scale,
            colorbar=dict(title='Salinity'),
            size=4
        ),
        hovertemplate='Time: %{x}<br>Salinity: %{y}',
        name=""
    ),
layout=go.Layout(
    width=700,
    height=550,
    title="Calvert Cliffs Nuclear Power Plant Salinity Levels",
    xaxis=dict(title="Time"),
    yaxis=dict(title="Salinity Levels"),
    showlegend=False
)
)



  SalinityPlotted.update_layout(
  yaxis_title="Salinity Levels",
  xaxis_title="Dates Samples Collected",
  title=f"<b>{marker_title}</b>", 
  title_x=0.5,
  yaxis_title_font=dict(
    size=18,
    family="Roboto"
      
    ),
    xaxis_title_font=dict(
    size=18,
    family="Roboto"
    ),
    
   
  )
  

  #This Creates The Time Series Data Slider 
  SalinityPlotted.update_layout(
     xaxis=dict(
        rangeselector=dict(
            buttons=list([
              #Creates button on top of graph to pick Specific Time Frames 
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=3,
                     label="3m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="todate"),
                dict(count=9,
                     label="9m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)


  graph_html = pio.to_html(SalinityPlotted, full_html=False,config=config)
  graph_json='<div id="graph_html">' + graph_html + '<div>'
  return jsonify({'graph_json': graph_json,})




  
