# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re

# Classes 
# Werden im dashboard mit "import utilities as ut" importiert und somit auch aufgerufen
class Subject():
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)

        self.subject_data = self.subject_data.interpolate(method='nearest', axis=0)

        __splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = ''.join(__splited_id)
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')
        



        

### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):
    return df.expanding(n).mean()
    

def calculate_SMA(df,n):
    return df.rolling(n).mean()


# Aufgabe 4
# 4.1 Sinnvoll bei Signalen mit hohem Rauschen und/oder kurzen Ausreißern. zB Aktienkurs bei Börsen
# Ungeeignet für Echtzeitsignale
# 4.2 Je größer n, desto mehr Anfangswerte können nicht berechnet werden und hohe Flanken im Signal werden starkt geglättet.