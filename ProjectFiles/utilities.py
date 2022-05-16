# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re

# Classes 

class Subject():
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)
<<<<<<< HEAD

        self.subject_data = self.subject_data.interpolate(method='nearest', axis=0)

=======
        self.subject_data = self.subject_data.interpolate(method='nearest', axis=0)
>>>>>>> c3ed91e820fd77c617986e4a756c8854f872ce5a
        __splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = ''.join(__splited_id)
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')
        #nn



        

### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):
    pass
    

def calculate_SMA(df,n):
    pass