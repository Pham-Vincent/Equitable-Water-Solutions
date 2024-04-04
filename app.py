""" 
Title:app.py
Author: Vincent Pham

Functionality: This Python program utilizes the google maps API Key to geoencode the Addresses -> Latitude and Longitude. This Program will take a csv file and turn it into a Dataframe. After this program will make an Google maps API call to geoencode the code and insert those values into a dataframe. After it has geoencoded all the addresses it will create a csv file with all the new Longitude and Latitude data

Output: CSV file 
Date:4/4/2024
"""



#Import necessary libraries
from flask import Flask,jsonify,render_template,request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64 

#Flask Instance
app = Flask(__name__)
#Allows to generate Graph Image 
plt.switch_backend('agg')

#Whenever a create_graph signal is sent will run this function
@app.route('/create_graph',methods=['GET', 'POST'])
def create_graph():
  years=np.array([2016,2017,2018,2019,2020])

  #Getting the JSON values 
  WithdrawValues = list(request.form.values())
  #Turns JSON Values Strings -> Floats
  WithdrawValues =[float(Floats) for Floats in WithdrawValues] 

  #creating the Plotting Style 
  plt.plot(years, WithdrawValues, marker='o',color='g',linestyle='-')
  plt.xlabel('Years')
  plt.ylabel('Water Withdraw')

  #Generating and Saving Image to display 
  img = io.BytesIO()
  plt.savefig(img,format="png")
  img.seek(0)
  plot_data = base64.b64encode(img.getvalue()).decode("utf-8")
  plt.close()
  return jsonify({'src': f'data:image/png;base64,{plot_data}', 'alt': 'Graph'})

#This will Render Our "HomePage" aka our Map 
@app.route('/',methods=['GET', 'POST'])
def index():
  return render_template('index.html')



if __name__ == '__main__':
  app.run(debug=True)
