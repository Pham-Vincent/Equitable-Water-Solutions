""" 
Title:app.py
Author: Vincent Pham

Functionality: This File purpose is to display different HTML files and allow for us to utilize python in our project. We will be able to send signals through javascript to Python to dynamically Load up different images or open up different html files. Currently it works to dynamically load Graphs. 


Output: Python Generated Images,Displays Webpage
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
