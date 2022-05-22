from cmath import nan
from tempfile import SpooledTemporaryFile
import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import utilities as ut
import numpy as np
import os
import re
from audioop import avg

app = Dash(__name__)


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
#print(folder_current) #= projekt files
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        #print(file_name)
        list_of_subjects.append(ut.Subject(file_name))

df = list_of_subjects[0].subject_data

grp=df[['SpO2 (%)','Temp (C)', 'Blood Flow (ml/s)']].agg(['max','idxmax','min','idxmin'])
print(grp)

df["BF_SMA"] = df["Blood Flow (ml/s)"].rolling(4).mean()
#df["Blood Flow (ml/s)"].rolling(5).mean()
bf_check = df.loc[2]
bf_check = bf_check

## Aufgabe 3.3
    alert_count = [] # 
    alert_sum = 0 #int, holds count of invalid values
    bf_SMA =  df["BF_SMA"]
    y_high = (df_avg.loc['Blood Flow (ml/s)'])*1.15
    y_low = (df_avg.loc['Blood Flow (ml/s)'])*0.85

    for i in bf_SMA:
        if i > y_high or i < y_low: # is simple moving average value '>' or '<' than the limit
            alert_count.append(bf.index[bf_SMA==i].tolist()) # append list of invalid values to list
            alert_sum += 1 #for each invalid value, alert_sum is going up by 1

    print('Alert count: ' + str(alert_count))
    print(str(alert_sum))
# y=grp.loc[['max','min','idxmax','idxmin']]
# index = y.loc['idxmax','SpO2 (%)']
# print(y)
# print(index)
# #x=grp.loc[['idxmax','idxmin']]
# #print(x)

# blood flow wird benötigt
# simple moving average
#bf = df['Blood Flow (ml/s)'].to_frame()
# spalte SMA30 wird geaddet
#bf['SMA30'] = bf['Blood Flow (ml/s)'].rolling().mean()
# removing all the null values
# bf.dropna(inplace=true)
#print(bf)

# cumulative moving average
#bf['CMA30'] = bf['Blood Flow (ml/s)'].expanding().mean()
#print(bf)
# Graph hinzufügen 
# fig.add_trace(go.Scatter(y=[4, 2, 1], mode="lines")

#3.1
#bf_avg=df[['Blood Flow (ml/s)']].agg(['mean','idxmean'])
#print(bf_avg)
#3.3
# def bloodflow_figure(value, bloodflow_checkmarks):

#     bf = list_of_subjects[int(value)-1].subject_data
#     bf["BF_SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"],5) 
#     bf_avg = bf.mean()
#     y_high = (bf_avg.loc['Blood Flow (ml/s)'])*1.15

#     y_high1= []
    
#     for element in bf['BF_SMA']:
#         if element > y_high:
#             y_high1.append(element)

#     print(y_high1)