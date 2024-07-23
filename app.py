
""" 
Title:app.py
Author: Vincent Pham

Functionality: The purpose of this file is to showcase various HTML files and enable the integration of Python into our project. Through JavaScript, we can transmit signals to Python, facilitating the dynamic loading of images or opening of different HTML files. Presently, it effectively supports the dynamic loading of graphs.


Output: Python Generated Images,Displays Webpage
Date:4/25/2024
"""


#Import necessary libraries

from flask import Flask,jsonify,render_template,request, redirect, url_for, session
from Database import *
from Graph import *
from login import *
from About import *
from FeatureExtraction import *
from dotenv import load_dotenv
import os
import pandas as pd
from flask_cors import CORS
#Path To Env File
dotenv_path='static/env/.env'
#Opens Env File
load_dotenv(dotenv_path=dotenv_path)

#Flask Instance
app = Flask(__name__)

#Allows app.route to Work For the Domain 
CORS(app)

#Secret Key used for Hashing
app.secret_key = os.getenv('SECRET_KEY')

#Purpose is to Return the Map API Key without revealing it to public
@app.route('/ApiKey')
def APIKEY():
    return(os.getenv('MAP_KEY'))

@app.route('/create_MultiDepth_graph',methods=['GET','POST'])
def create_MultiDepth_graph():
  #Gets Marker Title Of current Info Window From Ajax 
  marker_title = request.values
  #Gets Marker Title Name  
  marker_title = list(marker_title.keys())[0]

  #Establishes Connection With DB 
  conn = DatabaseConn()

  #Query For SQL
  mycursor = conn.cursor()

  Query = "SELECT Time, `Depth:0`,`Depth:5`,`Depth:10`,`Depth:15`,`Depth:20`,`Depth:25`,`Depth:30` FROM Maryland_Salinity_Depth WHERE PermitNumber = \"" + str(marker_title) + "\""
  #Executes The Query
  mycursor.execute(Query)
  #Get The Results of The Query
  myresult = mycursor.fetchall()
  column_names = ['Time', 'Depth:0', 'Depth:5', 'Depth:10', 'Depth:15', 'Depth:20', 'Depth:25', 'Depth:30']
  DepthDF = pd.DataFrame(myresult, columns=column_names)
  DepthDF['Time'] = pd.to_datetime(DepthDF['Time'])
  DepthDF=MonthlyAverages(DepthDF)
  return(MultiDepthGraphing(str(marker_title),DepthDF))



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
  Query = "SELECT Time, `Depth:0` FROM Maryland_Salinity_Depth WHERE PermitNumber = \"" + str(marker_title) + "\""
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
#Returns homepage with session variables
def index():
  if 'loggedin' in session:
      return render_template('index.html', username = session['username'])
  return render_template('index.html')
  
@app.route('/map', methods=['GET', 'POST'])
#Returns Map webpage
def map():
    checkLogin('map.html')
    return render_template('map.html')

#register page route
@app.route('/register', methods=['GET', 'POST'])
#Registers user and adds information to database
def register():
    return registerFunction()

#login page route
@app.route('/login', methods=['GET', 'POST'])
#Logs user in using information from database
def login():
    return loginFunction()

@app.route('/profile')
#Sets up profile page only when logged in
def profile():
    checkLogin('profile.html')
    return redirect(url_for('login'))


@app.route('/logout')
#deletes session variables
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('index'))

#Routing for the about us page
@app.route('/aboutus', methods=['GET', 'POST'])
#Function leads to about us page, sets up function call for the contact us section
def aboutus():
   return aboutusFunction()

def contactus():
   return contactusFunction()

#Routing for research paper page
@app.route('/researchpapers')
def research():
    checkLogin('research.html')
    return render_template('research.html')


if __name__ == '__main__':
  app.run(debug=True)


  
