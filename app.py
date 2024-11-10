
""" 
Title:app.py
Author: Vincent Pham, Nicholas Gammel

Functionality: The purpose of this file is to showcase various HTML files and enable the integration of Python into our project. 
Through JavaScript, we can transmit signals to Python, facilitating the dynamic loading of images or opening of different HTML files. 
It effectively supports the dynamic loading of graphs, supports a connection to the database for login/register/pinning.


Output: Python Generated Images,Displays Webpage
Date:4/25/2024
"""


#Import necessary libraries

from flask import Flask,jsonify,render_template,request, redirect, url_for, session, flash

from dotenv import load_dotenv
import os
import pandas as pd
from flask_cors import CORS
import sys

sys.path.append('static/python')
from Database import *
from Graph import *
from login import *
from About import *
from FeatureExtraction import *
from LocationPinning import * 

# AI Imports
from chatbot.scripts.chatbot import Chatbot
from chatbot.scripts.routes import setup_routes

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

openai_api_key = os.getenv('OPENAI_API_KEY')
chatbot = Chatbot(
  api_key=openai_api_key,
  project_name="Salinity",
)

setup_routes(app, chatbot)

#Purpose is to Return the Map API Key without revealing it to public
@app.route('/ApiKey')
def APIKEY():
    map_key = os.getenv('MAP_KEY')
    return jsonify({'mapKey': map_key})

# Route to create a heatmap for salinity at multiple depths
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


# Route to graph surface salinity of Maryland points
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
    if 'loggedin' in session:
        conn = DatabaseConn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where id = %s"
        cursor.execute(query, (session['id'],))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('profile.html', account=account)
    return render_template('index.html')

@app.route('/dashboard')
#Sets up dashboard page only when logged in
def dashboard():
    checkLogin('dashboard.html')
    return render_template('dashboard.html')


@app.route('/logout')
#deletes session variables
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Get the referring page URL
   referrer = request.referrer
   # Redirect to same page - logged out
   return redirect(referrer or url_for('index'))


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

@app.route('/antonia')
def antonia():
   return render_template('Antonia.html')
#returns the  information of the logged in user
@app.route('/session-data')
def sessionData():
  return(retrieve_sessionid())

#Utilized to Pin location into the Database
@app.route('/pin-location',methods=['POST'])
def pinLocation():
  return(add_pin_to_database(request.get_json()))

# Checks for override and duplication when pinning a marker
@app.route('/override',methods=['POST'])
def override():
  return overridecheck(request.get_json())


@app.route('/locations-pinned',methods=['POST'])
def pinnedLocations():
  return returnPinned(request.get_json())

@app.route('/verify_email/<token>')
def emailVer(token):
    return verify_email(token)

if __name__ == '__main__':
  app.run(debug=True)


  
