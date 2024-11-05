""" 
Title: Database.py
Author: Vincent Pham

Functionality: This file is designed to contain all functions related to Database. It includes a Function that is Used to connect to the Database.


Output: Database Connection
Date:6/21/2024
"""



from dotenv import load_dotenv
import mysql.connector
import os

#Function is used to establish a connection to Database
def DatabaseConn():
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

  return mydb


