
""" 
Title:Graph.py
Author: Vincent Pham

Functionality: This file is designed to contain all functions related to graphing. It includes functions that generate and return graphs for use in app.py.

Output: Python Generated Images
Date:6/20/2024
"""

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


#This Function is used to create the graph for Maryland
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


#This Function is Used to Graph the Viriginia Tidal Location
def Virginia_Tidal_Graph(WithdrawValues):
  config = {
  #Removes Plotly Logo On Graph
  'displaylogo': False,
  'editable':True,
  'modeBarButtonsToAdd':['resetcameradefault','resetViews'],
  'modeBarButtonsToRemove':['zoom2d', 'select2d', 'lasso2d', 'resetScale2d']
  }
 
  
  #Turns JSON Values Strings -> Floats
  WithdrawValues =[float(Floats) for Floats in WithdrawValues]

  year_strings =['2016','2017','2018','2019','2020']


  WithdrawValues_data = [[datetime.strptime(year, '%Y'), WithdrawValues[i]] for i, year in enumerate(year_strings)]
  WithdrawValues_df = pd.DataFrame(WithdrawValues_data,columns=['Years','WaterWithdraw'])
  
  #Creates a Scatter Plot 
  WithdrawPlotted = px.line(
    data_frame=WithdrawValues_df,
    y='WaterWithdraw',
    x='Years',
    orientation="v",
    width=700,
    height=550,
    markers = True,
      
)
  WithdrawPlotted.update_layout(
    title="Water Withdrawal Per Year", 
    title_x=0.5,
    title_font_family="Times New Roman",
  )
  #Visual Changes 
  WithdrawPlotted.update_traces(marker_size=10,marker_color='red',line_color='black')
  WithdrawPlotted.update_xaxes(title_font_family="Times New Roman")

  #Adding Slider Window And Buttons on top of the graph
  WithdrawPlotted.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="todate"),
                dict(count=2,
                     label="2y",
                     step="year",
                     stepmode="todate"),
                dict(count=3,
                     label="3y",
                     step="year",
                     stepmode="todate"),
                dict(count=4,
                     label="4y",
                     step="year",
                     stepmode="todate"),
                 dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
  )




  #Generating and Saving Image to display 
  graph_html = pio.to_html(WithdrawPlotted, full_html=False,config=config)
  graph_json='<div id="graph_html">' + graph_html + '<div>'
  return jsonify({'graph_json': graph_json,})
  
