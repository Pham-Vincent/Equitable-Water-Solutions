ears=np.array([2016,2017,2018,2019,2020])
  WithdrawValues = list(request.form.values())
  WithdrawValues =[float(Floats) for Floats in WithdrawValues] 
  plt.plot(years, WithdrawValues, marker='o',color='g',linestyle='-')
 
  plt.xlabel('Years')
  plt.ylabel('Water Withdraw')
  print(WithdrawValues)
  img = io.BytesIO()
  plt.savefig(img,format="png")