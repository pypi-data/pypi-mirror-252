import sys
import re
import pandas as pd
import numpy as np
def input_check(n):
  if len(sys.argv)!=n:
    print(f"Correct Usage: python {sys.argv[0]} <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    sys.exit(1)
  pattern=re.compile(r'^[a-zA-Z0-9_-]+\.csv$')
  if not pattern.match(sys.argv[1]):
      print("Error: Invalid <InputDataFile> format. Must be of the format 'name.csv'")
      print(f"Correct Usage: python {sys.argv[0]} <InputDataFile> <Weights> <Impacts> <ResultFileName>")
      sys.exit(1)
  if not pattern.match(sys.argv[4]):
      print("Error: Invalid <ResultFileName> format. Must be of the format 'name.csv'")
      print(f"Correct Usage: python {sys.argv[0]} <InputDataFile> <Weights> <Impacts> <ResultFileName>")
      sys.exit(1)  
  try:
    [float(i) for i in sys.argv[2].split(',')]
  except ValueError:
    print("Error: Weights must be comma-separated floats.")
    sys.exit(1)
  if sys.argv[3].count(',')==0:
    print("Error: Impacts must be comma-separated.")
    sys.exit(1)
  if not all(i in ['+','-'] for i in [i.strip() for i in sys.argv[3].split(',')]):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)
def data_load(inputFileName):
  try:
    input=pd.read_csv(inputFileName)
    return input
  except FileNotFoundError:
    print(f"Error: File {inputFileName} not found. Please check the file name and try again.")
    sys.exit(1)
  except pd.errors.EmptyDataError:
    print(f"Error: File {inputFileName} is empty. Please check the file and try again.")
    sys.exit(1)
def valid_data(input):
  if len(input.columns)<3:
    print("Error: Insufficient Columns. Input file must contain three or more columns.")
    sys.exit(1)
  num=0
  for i in input.columns[1:]:
    num+=1
    if pd.api.types.is_numeric_dtype(input[i].dtype)==False:
      print(f"Error: Column {num} has non-numeric data type. 2nd to last columns must contain numeric values only.")
      sys.exit(1)
def square(x):
  return x*x
def topsis(inputFileName,Weights,Impacts,resultFileName):
  input=data_load(inputFileName)
  valid_data(input)
  data=input.iloc[:,1:]
  cnum=data.shape[1]
  rnum=data.shape[0]
  cnames=data.columns
  weight=[float(i) for i in Weights.split(',')]
  impact=[i.strip() for i in Impacts.split(',')]
  if ((len(weight)!=len(impact))|(len(weight)!=cnum)):
    print("Error: Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
    sys.exit(1)
  for i in cnames:
    data[i]/=data[i].apply(square).sum()**0.5
  for i in range(cnum):
    data[cnames[i]]*=weight[i]
  best=list(np.zeros(cnum))
  worst=list(np.zeros(cnum))
  for i in range(cnum):
    if impact[i]=='+':
      best[i]=data[cnames[i]].max()
      worst[i]=data[cnames[i]].min()
    else:
      best[i]=data[cnames[i]].min()
      worst[i]=data[cnames[i]].max()
  best_dist=list(np.zeros(rnum))
  worst_dist=list(np.zeros(rnum))
  for i in range(rnum):
    for j in range(cnum):
      best_dist[i]=(data.iloc[i]-best).apply(square).sum()**0.5
      worst_dist[i]=(data.iloc[i]-worst).apply(square).sum()**0.5
  data['Si+']=best_dist
  data['Si-']=worst_dist
  data['Score']=data['Si-']/(data['Si+']+data['Si-'])
  input['Topsis Score']=(data['Score']*100).round(2)
  input['Rank']=input['Topsis Score'].rank(ascending=False).astype(int)
  input.to_csv(resultFileName,index=False)
if __name__ == "__main__":
  input_check(5)
  inputFile=sys.argv[1]
  weights=sys.argv[2]
  impacts=sys.argv[3]
  resultFile=sys.argv[4]
  topsis(inputFile,weights,impacts,resultFile)
