
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


#                            Maryland  Graphs 
#<-------------------------------------------------------------------------------------->
#This Function is used to create the graph for Maryland
def Maryland_Tidal_Graph(marker_title,Salinity_df):

  #Interacts with ModeBar
  config = {'displaylogo': False,}

  #creates The colorscale for Graph Currently Blue -> Red 
  color_scale = px.colors.diverging.Portland


#                       Creating the Graph + Adding the Color Scale
#<-------------------------------------------------------------------------------------->
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
        hovertemplate='Time: %{x}<br>Salinity: %{y} ppt',
        name=""
    ),
    # Define the layout
    layout=go.Layout(
        width=800,
        height=550,
        xaxis=dict(
            title="Timestamps",
            title_font=dict(
                size=18,
                family="Roboto"
            ),
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1 month",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3 months",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6 months",
                         step="month",
                         stepmode="todate"),
                    dict(count=9,
                         label="9 months",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        yaxis=dict(
            title="Salinity Levels",
            title_font=dict(
                size=18,
                family="Roboto"
            )
        ),
        title={
            'text': "<b>2022 Surface Salinity Information</b>",
            'x': 0.7
        },
        showlegend=False
    )
)

  
        
  graph_html = pio.to_html(SalinityPlotted, full_html=False,config=config)
  graph_json='<div id="graph_html">' + graph_html + '<div>'
  return jsonify({'graph_json': graph_json,})

#                            Virginia Graphs 
#<-------------------------------------------------------------------------------------->

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
  
  WithdrawPlotted = px.line(
    data_frame=WithdrawValues_df,
    y='WaterWithdraw',
    x='Years',
    width=700,
    height=550,
    markers=True
).update_layout(
    title="Water Withdrawal Per Year", 
    title_x=0.5,
    title_font_family="Times New Roman",
    xaxis=dict(
        title_font_family="Times New Roman",
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="todate"),
                dict(count=2, label="2y", step="year", stepmode="todate"),
                dict(count=3, label="3y", step="year", stepmode="todate"),
                dict(count=4, label="4y", step="year", stepmode="todate"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
).update_traces(
    marker_size=10,
    marker_color='red',
    line_color='black'
)



  #Generating and Saving Image to display 
  graph_html = pio.to_html(WithdrawPlotted, full_html=False,config=config)
  graph_json='<div id="graph_html">' + graph_html + '<div>'
  return jsonify({'graph_json': graph_json,})

# This function creates a heatmap to display salinity values at different depths
def MultiDepthGraphing(marker_title,Depth_df):
  #Color Scale For HeatMap
  custom_colorscale = [
      [0.0, '#9597c2'],    # Lightest blue
      [0.2, '#5b60b0'],   # Lighter blue
      [0.4, '#474b96'],   # Light blue
      [0.6, '#1d1f80'],   # Dark blue
      [0.8, '#0f1180'],   # Blue
      [1.0, '#030582']   # Dark blue
  ]
  config = {'displaylogo': False,}

  #Selects only the Depths That Want to be plotted
  Depth_df = Depth_df[['Time', 'Depth:0', 'Depth:5', 'Depth:10', 'Depth:15', 'Depth:20', 'Depth:25', 'Depth:30']]

  #Transposes the DataFrame to be in graphable form
  Depth_df = Depth_df.transpose()

  #Reorders The DataFrame as it gets Automatically Sorted in alphabetical order when grouping by month
  Depth_df = Depth_df[[4,3,7,0,8,6,5,1,11,10,9,2]]

  #Months Go In their own DF
  new_index = Depth_df.iloc[0]

  #Removes Months from DF
  Depth_df= Depth_df[1:]

  #Changes Names from Depth:0 -> 0 
  Depth_df.index=[0,5,10,15,20,25,30]
  Depth_df.columns = new_index
  #Graphing of the DataFrame
  fig = px.imshow(Depth_df, color_continuous_scale=custom_colorscale, aspect="auto")
  fig.update_layout(
      title= '<b>2022 Depth Salinity Information</b>',
      title_x=0.42,
      width=900,
      height=550,
      yaxis_title='Depth',
      xaxis_title='Timestamps',
      coloraxis_colorbar=dict(
          title='PPT<br>(Parts Per Thousand)',  # Title for the color bar
          title_side='top'                   # Position the title at the top
      ),
      yaxis_title_font=dict(
        size=16,
        family="Roboto",
          
      ),
      xaxis_title_font=dict(
        size=16,
        family="Roboto",
      ),
  ).update_traces(
      hovertemplate='<br>Month: %{x}<br>Depth: %{y}<br>Salinity: %{z}<extra></extra>',

  )

  graph_html = pio.to_html(fig, full_html=False,config=config)
  Depth_json='<div id="DepthHeatMap_html">' + graph_html + '<div>'
  return jsonify({'Depth_json': Depth_json,})
      