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

  Query = "Update Water_Data.Location_Pinned SET PinnedLocation" +str(data['pinNumber']) +"=" + "\"" + str(data['hydrocode']) + "\" WHERE id = \"" + str(data['userid']) + "\""
 
  
  #Executes The Query
  mycursor.execute(Query)
  conn.commit()  

  return "Success"
def overridecheck(data):
  #Establishes Connection With DB
  conn = DatabaseConn()
  #Query For SQL
  mycursor = conn.cursor()
  #Checks if any location is in the Location
  Query = "SELECT PinnedLocation" + str(data['pinNumber']) + " FROM Water_Data.Location_Pinned WHERE id = \"" + str(data['userid']) + "\""
  print(Query)
  mycursor.execute(Query)
  result = mycursor.fetchone()
  print(result)
  if(result[0] != None):
    return jsonify({'Current':result[0]})
  else:
    Query = "SELECT * FROM Water_Data.Location_Pinned WHERE id = \"" + str(data['userid']) + "\""
    mycursor.execute(Query)
    result = mycursor.fetchall()
    
    for row in result[0]:
      print(row)  # This will print the tuple
  
      if data['hydrocode'] == row:
          print('Duplicate found')
    return jsonify({'result':'true'})


  

