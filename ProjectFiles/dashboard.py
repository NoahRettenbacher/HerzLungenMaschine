from audioop import avg
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

colors = {
    'background': '#3e405f',
    'text':  ' #c1c3d8',
    'dropdown': "#7981f3"
}


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['min','max']
blood_flow_functions = ['CMA','SMA','Show Limits','Average']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

app.layout = html.Div(children=[
    html.H1(children='Cardiopulmonary Bypass Dashboard', style={'color': colors['text']}),

    html.Div(children='''
        Select the Patient ID 
    '''),
    
    html.Div([
        dcc.Dropdown(options = subj_numbers, placeholder='Select a subject', value='1', id='subject-dropdown', style={'BackgroundColor': colors['dropdown']}),
    html.Div(id='dd-output-container')
    ],
        style={"width": "5%"}
    ),


  #Min, Max
    dcc.Checklist(style={'Color': colors['text'],'BackgroundColor': colors['background']},
        id= 'checklist-algo',
        options=algorithm_names,
        inline=False
        ),
        

    dcc.Graph(
        id='dash-graph0',
        figure=fig0
    ),

    dcc.Graph(
        id='dash-graph1',
        figure=fig1
    ),

    dcc.Graph(
        id='dash-graph2',
        figure=fig2
    ),

    dcc.Checklist(
        id= 'checklist-bloodflow',
        options=blood_flow_functions,
        inline=False
    ),
    dcc.Graph(
        id='dash-graph3',
        figure=fig3
    )
])
### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)
def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])

    # fig0.update_layout(
    # plot_bgcolor=colors['background'],
    # paper_bgcolor=colors['background'],
    # font_color=colors['text']
    # )

    # fig1.update_layout(
    # plot_bgcolor=colors['background'],
    # paper_bgcolor=colors['background'],
    # font_color=colors['text']
    # )

    # fig2.update_layout(
    # plot_bgcolor=colors['background'],
    # paper_bgcolor=colors['background'],
    # font_color=colors['text']
    # )

    # fig3.update_layout(
    # plot_bgcolor=colors['background'],
    # paper_bgcolor=colors['background'],
    # font_color=colors['text']
    # )
    
    ### Aufgabe 2: Min / Max ###

    grp=ts[['SpO2 (%)','Temp (C)', 'Blood Flow (ml/s)']].agg(['max','idxmax','min','idxmin'])

    extrema=grp.loc[['max','min','idxmax','idxmin']]
    #print(extrema)

    # Markers on min and max in Dashboard 
    if 'max' in algorithm_checkmarks:
        fig0.add_trace(go.Scatter(x= [extrema.loc['idxmax','SpO2 (%)']], y = [extrema.loc['max','SpO2 (%)']],
                    mode='markers', name='max', marker_color= 'green'))

        fig1.add_trace(go.Scatter(x= [extrema.loc['idxmax','Blood Flow (ml/s)']], y = [extrema.loc['max','Blood Flow (ml/s)']],
                    mode='markers', name='max', marker_color= 'green'))

        fig2.add_trace(go.Scatter(x= [extrema.loc['idxmax','Temp (C)']], y = [extrema.loc['max','Temp (C)']],
                    mode='markers', name='max', marker_color= 'green'))

    if 'min' in algorithm_checkmarks:
        fig0.add_trace(go.Scatter(x= [extrema.loc['idxmin','SpO2 (%)']], y = [extrema.loc['min','SpO2 (%)']],
                    mode='markers', name='min', marker_color= 'red'))

        fig1.add_trace(go.Scatter(x= [extrema.loc['idxmin','Blood Flow (ml/s)']], y = [extrema.loc['min','Blood Flow (ml/s)']],
                    mode='markers', name='min', marker_color= 'red'))

        fig2.add_trace(go.Scatter(x= [extrema.loc['idxmin','Temp (C)']], y = [extrema.loc['min','Temp (C)']],
                    mode='markers', name='min', marker_color= 'red'))
        
    return fig0, fig1, fig2 


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    ## Hier ut. aufrufen (= utilities.py)
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")

    # fig3.update_layout(
    # plot_bgcolor=colors['background'],
    # paper_bgcolor=colors['background'],
    # font_color=colors['text']
    # )
    

    bf["BF_SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"],4) 

    if bloodflow_checkmarks is not None: 
        # simple moving average
        if 'SMA' in bloodflow_checkmarks:
            #bf["BF_SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"],5) 
            fig3.add_trace(go.Scatter(x=bf["Time (s)"],y=bf["BF_SMA"],mode='lines', marker_color = 'orange', name= 'SMA'))
            #fig3.add_trace(go.Scatter(y=bf.loc['BF_SMA'], mode="lines"))          
            
        # cumulative moving average
        if 'CMA' in bloodflow_checkmarks:
            bf["BF_CMA"] = ut.calculate_CMA(bf["Blood Flow (ml/s)"],3) 
            fig3.add_trace(go.Scatter(x=bf["Time (s)"],y=bf["BF_CMA"],mode='lines', marker_color = 'turquoise', name= 'CMA'))

        #Aufgabe 3.1 average Blood Flow:
        if 'Show Limits' in bloodflow_checkmarks:
            #bf_avg=df[['Blood Flow (ml/s)']].agg(['mean','idxmean'])
            bf_avg = bf.mean()
            x= [0,480]
            y=bf_avg.loc['Blood Flow (ml/s)']

            #3.2 15% Intervalls
            y_high = (bf_avg.loc['Blood Flow (ml/s)'])*1.15
            fig3.add_trace(go.Scatter(x = x, y = [y_high,y_high],mode = 'lines', marker_color = 'green', name = 'upper Limit'))

            y_low = (bf_avg.loc['Blood Flow (ml/s)'])*0.85
            fig3.add_trace(go.Scatter(x = x, y = [y_low,y_low],mode = 'lines', marker_color = 'red', name = 'lower Limit'))

        if 'Average' in bloodflow_checkmarks:
            bf_avg = bf.mean()
            x= [0,480]
            y=bf_avg.loc['Blood Flow (ml/s)']
            #scatter methode 
            fig3.add_trace(go.Scatter(x=x,y=[y,y],mode='lines', marker_color = 'violet', name= 'Average'))



    # Aufgabe 3.3
   
    # alert_sum = 0 #int, holds count of invalid values
    # bf_SMA = bf["BF_SMA"]

    # for i in bf_SMA:
    #     if i > y_high or i < y_low: # is simple moving average value '>' or '<' than the limit
    #         #alert_count.append(bf.index[bf_SMA==i].tolist()) # append list of invalid values to list
    #         alert_sum += 1 #for each invalid value, alert_sum is going up by 1

    # print(str(alert_sum))

    # # Defining alert message shown in textarea


    

    return fig3


    
    
    

if __name__ == '__main__':
    app.run_server(debug=True)


# Theoretische Antworten 
# 3.4 Bei großen n wird ein hoher andauernder Bloodflow erst spät erkannt, deswegen muss n so gesetzt werden, dass Außreiser unterhalb des Limits bleiben, aber hohe andauernde Werte schon.
# Aufgrund dessen wird n = 4 gewählt.