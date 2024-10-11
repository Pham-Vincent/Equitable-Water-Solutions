#This File will Contain All the Functions Utilized for location Pinning 
from flask import Flask,jsonify,render_template,request, redirect, url_for, session
from Database import *


#Utilized to get the Current Userid returns to MarkerPinning.js
def retrieve_sessionid():
  if 'loggedin' in session:
    return {'id': session.get('id', '')}
  else:
    return {'id': None}

def add_pin_to_database(data):
  #Establishes Connection With DB
  conn = DatabaseConn()
  #Query For SQL
  mycursor = conn.cursor()
  Query = "SELECT PinnedLocation1,PinnedLocation2,PinnedLocation3,PinnedLocation4,PinnedLocation5 FROM Location_Pinned WHERE id = \"" + str(data['userid']) + "\""
  #Executes The Query
  mycursor.execute(Query)
  result= mycursor.fetchall()
  print("HI")
  print(result)



  return(None)