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

# grp=df[['SpO2 (%)','Temp (C)', 'Blood Flow (ml/s)']].agg(['max','idxmax','min','idxmin'])
# #print(grp)
# y=grp.loc[['max','min','idxmax','idxmin']]
# index = y.loc['idxmax','SpO2 (%)']
# print(y)
# print(index)
# #x=grp.loc[['idxmax','idxmin']]
# #print(x)

# blood flow wird benötigt
# simple moving average
bf = df['Blood Flow (ml/s)'].to_frame()
# spalte SMA30 wird geaddet
bf['SMA30'] = bf['Blood Flow (ml/s)'].rolling(15).mean()
# removing all the null values
# bf.dropna(inplace=true)
print(bf)

# cumulative moving average
bf['CMA30'] = bf['Blood Flow (ml/s)'].expanding().mean()
print(bf)
# Graph hinzufügen 
# fig.add_trace(go.Scatter(y=[4, 2, 1], mode="lines")

