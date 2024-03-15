from flask import Flask,jsonify,render_template,request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64 


app = Flask(__name__)
plt.switch_backend('agg')
@app.route('/create_graph',methods=['GET', 'POST'])
def create_graph():
  years=np.array([2016,2017,2018,2019,2020])
  WithdrawValues = list(request.form.values())
  plt.plot(years, WithdrawValues, marker='o',color='g',linestyle='-')
  plt.title("HEY")
  plt.xlabel('Years')
  plt.ylabel('Water Withdraw')
  img = io.BytesIO()
  plt.savefig(img,format="png")
  img.seek(0)
  plot_data = base64.b64encode(img.getvalue()).decode("utf-8")
  return jsonify({'src': f'data:image/png;base64,{plot_data}', 'alt': 'Graph'})
  
@app.route('/',methods=['GET', 'POST'])
def index():
  return render_template('index.html')



if __name__ == '__main__':
  app.run(debug=True)
