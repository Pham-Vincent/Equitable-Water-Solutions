
""" 
Title:app.py
Author: Vincent Pham

Functionality: The purpose of this file is to showcase various HTML files and enable the integration of Python into our project. Through JavaScript, we can transmit signals to Python, facilitating the dynamic loading of images or opening of different HTML files. Presently, it effectively supports the dynamic loading of graphs.


Output: Python Generated Images,Displays Webpage
Date:4/25/2024
"""


#Import necessary libraries
from flask import Flask,jsonify,render_template,request, redirect, url_for
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
from flask_bcrypt import generate_password_hash

#Flask Instance
app = Flask(__name__)
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

#test database connection
conn = mysql.connector.connect(**db_config)

def connect_to_database():
    return mysql.connector.connect(**db_config)

#register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not username or not password or not email:
            error = 'Please fill out all fields'
            return render_template('register.html', error=error)
        elif check_existing_user(username):
            error = 'Username already exists'
            return render_template('register.html', error=error)
        elif check_existing_email(email):
            error = 'Email already exists'
            return render_template('register.html', error=error)
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password).decode('utf-8')
            add_user(username, hashed_password, email)
            return redirect(url_for('index'))  # Redirect to home page after successful registration
    return render_template('register.html')

# Function to check if username already exists
def check_existing_user(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "SELECT * FROM Accounts WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def check_existing_email(email):
   conn = connect_to_database()
   cursor = conn.cursor()
   query = "SELECT * FROM Accounts WHERE email = %s"
   cursor.execute(query, (email,))
   user = cursor.fetchone()
   cursor.close()
   conn.close()
   return user is not None

# Function to add a new user to the database
def add_user(username, password, email):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "INSERT INTO Accounts (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
  app.run(debug=True)
