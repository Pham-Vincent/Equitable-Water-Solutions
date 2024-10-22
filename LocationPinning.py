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

  mycursor.execute(Query)
  result = mycursor.fetchone()
  #if result is not empty, it means either a duplicate exists or the entry needs to be overridden
  #checks for a duplicate, and if found, returns it; otherwise, returns that the entry needs to be overridden
  if(result[0] != None):
    #Returns What error it is for and the Hydrocde that needs to be overridden
    Query = "SELECT * FROM Water_Data.Location_Pinned WHERE id = \"" + str(data['userid']) + "\""
    mycursor.execute(Query)
    result = mycursor.fetchall()
    
    #Checks if it finds a Duplicate
    for index,row in enumerate(result[0]):
      if data['hydrocode'] == row:
          print('Duplicate found')
          return({'error':'dupe','dupeLocation': index})
    #Otherwise Returns override error
    return jsonify({'error':'override','override':result[0],})
  else:
    #Nothing in that Pinnedlocation so can pin
    return jsonify({'result':'true'})

def returnPinned(data):
  #Establishes Connection With DB
  conn = DatabaseConn()
  #Query For SQL
  mycursor = conn.cursor()
  Query = "SELECT PinnedLocation1,PinnedLocation2,PinnedLocation3 FROM Water_Data.Location_Pinned WHERE id = \"" + str(data['userid']) + "\""
  mycursor.execute(Query)
  result = mycursor.fetchall()
  

  return jsonify(result)



  

