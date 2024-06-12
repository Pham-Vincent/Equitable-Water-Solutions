from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import numpy as np

#Each dataPoint will Get a 1 week span From Current Date looking
def CreateWindow(DataFrame):
  df = pd.DataFrame(columns=['Mean','STD','Window'])
  # 1 week is 168 Points
  WindowSize = 168
  

  for i in range(len(DataFrame)):
      # Span of days before Current Point (3.5 days)
      BeforeDate = max(0, i - (WindowSize // 2))
      # Span of Days After Current Point (3.5 days)
      AfterDate = min(len(DataFrame), i + (WindowSize // 2))

      # Will get All Values From Index BeforeDate to AfterDate
      Window = DataFrame[BeforeDate:AfterDate]


      WindowList = Window['Salinity'].astype(float).values.tolist()
      df.loc[i,'Window'] = [WindowList]
      df.loc[i,'Mean']= np.mean(WindowList)
      df.loc[i,'STD']= np.std(WindowList)
      # DataFrame.at[i, 'Window'] = WindowList
  DataFrame = pd.concat([DataFrame, df], axis=1)
  print(DataFrame)

  return(DataFrame)



def Variance(DataFrame):
  print('Hi')

def AvgNeighbors(DataFrame):

    #Calculates For closest 24 Neighbors 
    k = 24

    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(X)

    # Find indices and distances of k nearest neighbors
    distances, indices = knn.kneighbors(X, n_neighbors=k+1)

    # Calculate average distance
    for i,pred in enumerate(distances):
      #Calculates the Avg Distance Between Neighbors
      avg_distance = np.mean(distances[i])


      #Inserting Data into Anamoly DF 
      Salinity_df.loc[i, 'AvgNeighbor'] = avg_distance


def main():
  # Path To Get Environment Variables
  dotenv_path = 'static/env/.env'
  # Getting Environment Variables
  load_dotenv(dotenv_path=dotenv_path)

  # Connecting to Database
  mydb = mysql.connector.connect(
      host=os.getenv('DB_HOST'),
      user=os.getenv('DB_USER'),
      password=os.getenv('DB_PASS'),
      database=os.getenv('DB_NAME')
  )
  mycursor = mydb.cursor()
  # Query To Get Desired Values from Database
  query = "SELECT time, Salinity FROM Maryland_Tidal_History WHERE PermitNumber = 'CA1971S001(04)'"

  # Executing Query
  mycursor.execute(query)

  # Getting Results From Query
  myresult = mycursor.fetchall()

  # Inserting The Data Into DataFrame
  Salinity_data = [[Time, Salinity] for Time, Salinity in myresult]
  Salinity_df = pd.DataFrame(Salinity_data, columns=['Time', 'Salinity'])
  Salinity_df['Time'] = pd.to_datetime(Salinity_df['Time']).apply(lambda x: x.timestamp())

  X = Salinity_df[['Time', 'Salinity']]

  #Gets Features and Window 
  X = CreateWindow(Salinity_df)
  X.drop(['Window','Time'],axis =1, inplace = True)

  

  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)
  # Outlier Detection Process
  clf = svm.OneClassSVM(nu=0.05, kernel="rbf", gamma=.1).fit(X_scaled)
  y_predict = clf.predict(X_scaled)

  # Making 1 be Outlier and 0 be Normal
  svm_predict = pd.Series(y_predict, index=Salinity_df.index).replace([-1, 1], [1, 0])

  mycursor.close()
  mydb.close()

  # Mark the outliers and normal points
  outliers = X[svm_predict == 1].values
  normal_data = X[svm_predict == 0].values



  svm_anomalies=pd.DataFrame(columns=["Salinity","Time"])
  #Creating a DF where only the Salinity has Points to Graph Later
  for i,pred in enumerate(svm_predict):
    #Normal So No Data Needed For Anamoly DataFrame
    if pred == 0:
      svm_anomalies.loc[i, :] = None
    else:
      Salinity = Salinity_df.loc[i,'Salinity']
      Time = Salinity_df.loc[i,'Time']
      
      #Inserting Data into Anamoly DF 
      svm_anomalies.loc[i, 'Salinity'] = Salinity
      svm_anomalies.loc[i,'Time']=Time

  #Converting the Time To Be Readable
  Salinity_df['Datetime'] = pd.to_datetime(Salinity_df['Time'], unit='s')
  svm_anomalies['Datetime'] = pd.to_datetime(svm_anomalies['Time'], unit='s')


  SalinityPlotted = go.Figure()

  SalinityPlotted.add_trace(go.Scatter(
      x=Salinity_df['Datetime'],
      y=Salinity_df['Salinity'],
      mode='lines',
      name='Salinity',
      hovertemplate='Time %{x}<br>Salinity: %{y}',
      connectgaps=False
  ))

  SalinityPlotted.add_trace(go.Scatter(
      x=svm_anomalies['Datetime'],
      y=svm_anomalies['Salinity'],
      mode='lines',
      marker=dict(color='red', size=8),
      name='Anomaly',
      hovertemplate='Time %{x}<br>Salinity: %{y}'
  ))

  SalinityPlotted.update_layout(
      width=700,
      height=550,
      title="Calvert Cliffs Nuclear Power Plant Salinity Levels",
      xaxis=dict(title="Time"),
      yaxis=dict(title="Salinity Levels"),
      showlegend=True
  )

  SalinityPlotted.update_layout(
      yaxis_title="Salinity Levels",
      xaxis_title="Dates Samples Collected",
      title=f"<b>Calvert Cliffs Nuclear Power Plant Salinity Levels</b>",
      title_x=0.5,
      yaxis_title_font=dict(size=18, family="Roboto"),
      xaxis_title_font=dict(size=18, family="Roboto"),
  )

  #Time Series Data Creation
  SalinityPlotted.update_layout(
      xaxis=dict(
          rangeselector=dict(
              buttons=list([
                  dict(count=1, label="1m", step="month", stepmode="backward"),
                  dict(count=3, label="3m", step="month", stepmode="backward"),
                  dict(count=6, label="6m", step="month", stepmode="todate"),
                  dict(count=9, label="9m", step="month", stepmode="backward"),
                  dict(step="all")
              ])
          ),
          rangeslider=dict(visible=True),
          type="date"
      )
  )
  SalinityPlotted.show()  



main()