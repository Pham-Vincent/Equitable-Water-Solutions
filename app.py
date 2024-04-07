""" 
Title:app.py
Author: Vincent Pham

Functionality: This File purpose is to display different HTML files and allow for us to utilize python in our project. We will be able to send signals through javascript to Python to dynamically Load up different images or open up different html files. Currently it works to dynamically load Graphs. 


Output: Python Generated Images,Displays Webpage
Date:4/4/2024
"""



#Import necessary libraries
from flask import Flask,jsonify,render_template,request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64 
import pandas as pd
import plotly.express as px
import  plotly.io as pio
import plotly
#Flask Instance
app = Flask(__name__)
#Allows to generate Graph Image 
plt.switch_backend('agg')

#Whenever a create_graph signal is sent will run this function
@app.route('/create_graph',methods=['GET', 'POST'])
def create_graph():
  years=np.array([2016,2017,2018,2019,2020])

  #Getting the JSON values 
  WithdrawValues = list(request.form.values())
  #Turns JSON Values Strings -> Floats
  WithdrawValues =[float(Floats) for Floats in WithdrawValues]
  WithdrawValues_data = [['Year_2016',WithdrawValues[0]],['Year_2017',WithdrawValues[1]],['Year_2018',WithdrawValues[2]],['Year_2019',WithdrawValues[3]],['Year_2020',WithdrawValues[4]]]
  WithdrawValues_df = pd.DataFrame(WithdrawValues_data,columns=['Years','Values'])


  print(WithdrawValues_df)
  

  barchart=px.bar(
    data_frame = WithdrawValues_df,
    y='Values',
    x='Years',
    color = 'Values',
    opacity=.9,
    orientation ="v",
     width=800, 
     height=900
  )
  

  #Generating and Saving Image to display 
  graph_html = pio.to_html(barchart, full_html=False)
  graph_json='<div id="graph_html">' + graph_html + '<div>'
  return jsonify({'graph_json': graph_json})

#This will Render Our "HomePage" aka our Map 
@app.route('/',methods=['GET', 'POST'])
def index():
  return render_template('index.html')



if __name__ == '__main__':
  app.run(debug=True)
