
""" 
Title:app.py
Author: Vincent Pham

Functionality: The purpose of this file is to showcase various HTML files and enable the integration of Python into our project. Through JavaScript, we can transmit signals to Python, facilitating the dynamic loading of images or opening of different HTML files. Presently, it effectively supports the dynamic loading of graphs.


Output: Python Generated Images,Displays Webpage
Date:4/25/2024
"""


#Import necessary libraries
from flask import Flask,jsonify,render_template,request
from Database import *
from Graph import *
from FeatureExtraction import *
import numpy as np
import io
import os
import base64 
import pandas as pd
import mysql.connector

#Flask Instance
app = Flask(__name__)



@app.route('/create_MD_graph',methods=['GET','POST'])

def create_MD_graph():
  #Gets Marker Title Of current Info Window From Ajax 
  marker_title = request.values
  #Gets Marker Title Name  
  marker_title = list(marker_title.keys())[0]

  #Establishes Connection With DB 
  conn = DatabaseConn()

  mycursor = conn.cursor()

  #Query For SQL
  Query = "SELECT time,Salinity FROM Maryland_Tidal_History WHERE PermitNumber = \"" + str(marker_title)+ "\""

  #Executes The Query
  mycursor.execute(Query)

  #Get The Results of The Query
  myresult = mycursor.fetchall()

  Salinity_data = [[Time,Salinity] for Time,Salinity in (myresult)]
  Salinity_df= pd.DataFrame(Salinity_data,columns=['Time','Salinity'])

  Salinity_df=AverageDailySalinity(Salinity_df) 
  return(Maryland_Tidal_Graph(str(marker_title),Salinity_df))

  
#Whenever a create_graph signal is sent will run this function
@app.route('/create_VA_graph',methods=['GET', 'POST'])
def create_graph():
  #Getting the JSON values from current Marker that is being graphed 
  WithdrawValues = list(request.form.values())
  return Virginia_Tidal_Graph(WithdrawValues)




#This will Render Our "HomePage" aka our Map 
@app.route('/',methods=['GET', 'POST'])
def index():
  return render_template('index.html')




if __name__ == '__main__':
  app.run(debug=True)
