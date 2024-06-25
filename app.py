
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
from Database import *
from Graph import *
c

import numpy as np
import io
import os
import base64 
import pandas as pd
import hashlib, re

#Path To Env File
dotenv_path='static/env/.env'
#Opens Env File
load_dotenv(dotenv_path=dotenv_path)

#Flask Instance
app = Flask(__name__)

#Secret Key used for Hashing
app.secret_key = os.getenv('SECRET_KEY')





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
#Returns homepage with session variables
def index():

  if 'loggedin' in session:
      return render_template('index.html', username = session['username'])
  return render_template('index.html')
  
@app.route('/map', methods=['GET', 'POST'])
#Returns Map webpage
def map():
    if 'loggedin' in session:
      return render_template('map.html', username = session['username'])
    return render_template('map.html')

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

#Creates Database Connection
def connect_to_database():
    return mysql.connector.connect(**db_config)

#register page route
@app.route('/register', methods=['GET', 'POST'])
#Registers user and adds information to database
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
            query = "SELECT * FROM Accounts where username = %s AND password = %s"
            cursor.execute(query, (username, password,))
            account = cursor.fetchone()
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            cursor.close()
            conn.close()
            # Redirect to map page
            return redirect(url_for('index'))
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    msg=''
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
#Uses login submission to check database for matching information
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
            cursor.close()
            conn.close()
            # Redirect to map page
            return redirect(url_for('index'))
        else:
            cursor.close()
            conn.close()
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    msg=''
    return render_template('login.html', msg=msg)

@app.route('/profile')
#Sets up profile page only when logged in
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
#deletes session variables
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)
