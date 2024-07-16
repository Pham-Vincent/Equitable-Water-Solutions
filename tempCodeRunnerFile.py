 #Iterates Through Dates and Then Gets Average Salinity For Each Day  
  for i in enumerate(range(0,12)):
    #Gets all Salinity Values That are in a Certain Date 
    filtered_df = DataFrame[DataFrame['Time'].dt.date == CurrentDate.date()]

    #Converts Salinity DF to List With Float Variables
    Depth0 = filtered_df['Depth:0'].astype(float).values.tolist()
    Depth15 = filtered_df['Depth:15'].astype(float).values.tolist()
    Depth30 = filtered_df['Depth:30'].astype(float).values.tolist()

    CurrentDate = pd.to_datetime(CurrentDate, format='%Y-%m-%d')  
    
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:0'] = np.mean(Depth0)     
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:15'] = np.mean(Depth15)     
    NewDates.loc[NewDates['Time'] == CurrentDate, 'Depth:30'] = np.mean(Depth30)     
    print(NewDates)