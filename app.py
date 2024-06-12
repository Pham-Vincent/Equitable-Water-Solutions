
""" 
Title:app.py
Author: Vincent Pham

Functionality: The purpose of this file is to showcase various HTML files and enable the integration of Python into our project. Through JavaScript, we can transmit signals to Python, facilitating the dynamic loading of images or opening of different HTML files. Presently, it effectively supports the dynamic loading of graphs.


Output: Python Generated Images,Displays Webpage
Date:4/25/2024
"""


#Import necessary libraries
from flask import Flask,jsonify,render_template,request, redirect, url_for, session
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import io
from dotenv import load_dotenv
import os
import base64 
import pandas as pd
import plotly.express as px
import  plotly.io as pio
import plotly
from datetime import datetime
from plotly import graph_objs as go
import hashlib, re

#Path To Env File
dotenv_path='static/env/.env'
#Opens Env File
load_dotenv(dotenv_path=dotenv_path)

#Flask Instance
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

#Allows to generate Graph Image 
plt.switch_backend('agg')

#Interacts with ModeBar
config = {'displaylogo': False,}

@app.route('/create_MD_graph',methods=['GET','POST'])
def Hardcode_Graph():
  #Path To Env File
  dotenv_path='static/env/.env'
  #Opens Env File
  load_dotenv(dotenv_path=dotenv_path)
  #Connects to Database To Get Data
  mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user= os.getenv('DB_USER'),
    password= os.getenv('DB_PASS'),
    database= os.getenv('DB_NAME')

  )
  #Gets Marker Title Of current Info Window From Ajax 
  marker_title = request.values
  #Gets Marker Title Name 
  marker_title = list(marker_title.keys())[0]

  mycursor = mydb.cursor()

  #Query For SQL
  Query = "SELECT time,Salinity FROM Maryland_Tidal_History WHERE PermitNumber = \"" + str(marker_title)+ "\""

  #Executes The Query
  mycursor.execute(Query)

  #Get The Results of The Query
  myresult = mycursor.fetchall()
  

  Salinity_data = [[Time,Salinity] for Time,Salinity in (myresult)]
  Salinity_df= pd.DataFrame(Salinity_data,columns=['Time','Salinity'])
  
  SalinityPlotted = go.Figure(
    data=go.Scatter(
        x=Salinity_df['Time'],
        y=Salinity_df['Salinity'],
        mode='lines',
        name='',
        hovertemplate='Time %{x}<br>Salinity: %{y}',  # Custom hover text template
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
  
  SalinityPlotted.update_layout(
     xaxis=dict(
        rangeselector=dict(
            buttons=list([
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
  


  return
#Whenever a create_graph signal is sent will run this function
@app.route('/create_VA_graph',methods=['GET', 'POST'])
def create_graph():
  config = {
  #Removes Plotly Logo On Graph
  'displaylogo': False,
  'editable':True,
  'modeBarButtonsToAdd':['resetcameradefault','resetViews'],
  'modeBarButtonsToRemove':['zoom2d', 'select2d', 'lasso2d', 'resetScale2d']
  }
  #Getting the JSON values 
  WithdrawValues = list(request.form.values())
  
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




#This will Render Our "HomePage" aka our Map 
@app.route('/',methods=['GET', 'POST'])
def index():
  if 'loggedin' in session:
      print(session['username'])
      return render_template('index.html', username = session['username'])
  return render_template('index.html')
  


#Path To Env File
dotenv_path='static/env/.env'
#Opens Env File
load_dotenv(dotenv_path=dotenv_path)
#Connect to DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def connect_to_database():
    return mysql.connector.connect(**db_config)

#register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    #Checks that fields are filled
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #Creates database connection and executes query
        #Stores single sequence result in account
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        #Validates if the account exists and follows correct naming conventions
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            #CREATES NEW ACCOUNT
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Insert into Database
            query = "INSERT INTO Accounts (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            conn.commit()
            cursor.close()
            conn.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    msg=''
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Hashes input password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        #Creates database connection
        #Executes query to see if there is account with matching username and hashed password
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where username = %s AND password = %s"
        cursor.execute(query, (username, password,))
        account = cursor.fetchone()
        # If account exists in database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to map page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    msg=''
    return render_template('login.html', msg=msg)

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where id = %s"
        cursor.execute(query, (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(debug=True)
