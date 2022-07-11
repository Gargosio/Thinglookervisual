# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 10:47:09 2022

@author: TEVIN
"""

#Import Dependancies
import dash_bootstrap_components as dbc
import dash
#Sfrom dash.dependencies import Input,Output
import dash_daq as daq
from dash import dcc,html,dash_table
import plotly.express as px
import redis
import pandas as pd
#import time
from datetime import timedelta
from dash.dependencies import Input, Output
#import plotly.graph_objects as go


################
rc = redis.Redis(
    host="redis-15365.c277.us-east-1-3.ec2.cloud.redislabs.com",
    charset="utf-8",
    decode_responses=True,
    port=15365,
    password="ruqK6OVaQpYajpp1glVruZYZdTHQfMlq")



#Fetching from db
df = pd.DataFrame()
p = rc.pipeline()
for key in rc.keys():
    p.hgetall(key)
df = df.append(p.execute())
   ####################
   
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)
########################3
   
# df = pd.read_csv("data.csv")

#newDF = newDF.drop("index",axis=1)
# Transformations

# Eliminating test records
df = df.loc[(df['device'] == '1FA1A28')]


# Converting time, humidity and temperature into int
df['time'] = df['time'].astype(int)   # Transform as numeric
#df['time'] = pd.to_datetime(df['time'])
df['Humidity'] = df['Humidity'].astype(int)
df['Temperature'] = df['Temperature'].astype(int)

# check column data types
coltypes = df.dtypes
print(coltypes)

# Converting time from Epoch Unix to datetime
df['time'] = pd.to_datetime(df['time'], unit='s', utc=False)
df['time'] += timedelta(hours=3)

# Sorting data frame in descending order based on time
df = df.sort_values(by='time', ascending=False)

newDF = df.copy()
newDF = newDF.rename(columns = {'pk':'event_id', 'time':'event_time', 'Humidity':'Humidity (g.kg-1)',
                      'Temperature':'Temperature (°C)'}, inplace = False)

#getting aggrgates
avgTemp = round(df["Temperature"].mean(),2)
avgHumidity =  round(df["Humidity"].mean(),2)
minTemp = df["Temperature"].min()
maxTemp = df["Temperature"].max()
minHumidity = df["Humidity"].min()
maxHumidity = df["Humidity"].max()
NoReads = df["pk"].count()
# print(NoReads)
Deviceid = df.iloc[0,1]
# latestdate = str(df["time"].max())
# latestTimestamp = dt.strptime(latestdate, '%Y-%m-%d %H:%M:%S')
# latestTime = latestTimestamp.strftime('%H:%M:%S')

# visualizations

#plotting the gauge charts
#Humidity gauge chart
figtemp = px.area(df, x="time", y="Temperature",line_shape='spline',
                  title='Temperature Hourly Trend',
                  labels={
                     "time": "Time of Day",
                     "Temperature": "Temperature (°C)"
                 }
                  , color_discrete_sequence=["#cb4154"],height=325
                  )
figtemp.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'margin':{'l': 20, 'r': 20},
'font_color':"#ffffff",
'title_font_color':"#ffffff",
"title_font":{'size': 20},
})
figtemp.update_xaxes(showgrid=False)
figtemp.update_yaxes(showgrid=False)

fighum = px.area(df, x="time", y="Humidity",line_shape='spline',title='Humidity Hourly Trend',
                 labels={
                    "time": "Time of Day",
                    "Humidity": "Humidity (g.kg-1)"
                }
                 , color_discrete_sequence=["#cb4154"],height=325
                 )
fighum.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'margin':{'l': 20, 'r': 20},
'font_color':"#ffffff",
'title_font_color':"#ffffff",
"title_font":{'size': 20},
})
fighum.update_xaxes(showgrid=False)
fighum.update_yaxes(showgrid=False)


app.layout = dbc.Container(fluid=True,
                            children=[
    html.Div(
    [

     # html.P(),
     # html.P(),
     dbc.Card(
        dbc.Row(
            [
               html.P(),
               html.P(),  
     html.H4("DHT11 Sensor Analytics (Last 24 Hours)"
             ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#cb4154",}
             ),
     ]
            ),style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"},),
     
     
     html.P(),
     html.P(),
     dbc.Card(
        dbc.Row(
            [
##########

####Device Device card
dbc.Col(dbc.Card([
        dbc.CardHeader("Device ID",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(Deviceid,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff"}, className="card-title"),
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        #dbc.CardFooter("This is the footer"),
    ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
   
    ),xs=6,sm=4,md=4,lg=2,xl=2,
    style = {"margin-top":"1%",}),

#### No of Hits card
    dbc.Col(dbc.Card([
    dbc.CardHeader("Data Reads",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                        "text-align":"center","color":"#ffffff","font-weight":"bold",}),
    dbc.CardBody(
        [
            html.H4(id="load_Noreads",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                "text-align":"center","color":"#ffffff"}, className="card-title"),
            dcc.Interval(id='interval-read-component',n_intervals=65*1000,)
           # html.P("This is some card text", className="card-text"),
        ]
    ),
    #dbc.CardFooter("This is the footer"),
],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
), xs=6,sm=4,md=4,lg=2,xl=2,
style = {"margin-top":"1%",}),
       
        dbc.Col(dbc.Card([
        dbc.CardHeader("Max Humidity",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_maxHumidity",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff"}, className="card-title"),
                dcc.Interval(id='interval-mhum-component',n_intervals=150*1000,),
                #html.P("This is some card text", className="card-text"),
            ],
        ),
        dbc.CardFooter("(g.kg-1)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
    ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
   ), xs=6,sm=4,md=4,lg=2,xl=2,
   style = {"margin-top":"1%",}),
        ##########################
     
        dbc.Col(dbc.Card([
        dbc.CardHeader("Max Temperature",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_maxTemperature", style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff"},  className="card-title"),
                dcc.Interval(id='interval-maxtemp-component',n_intervals=205*1000,),
                #html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter("(°C)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
    ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
    ), xs=6,sm=4,md=4,lg=2,xl=2,
    style = {"margin-top":"1%",}),
       
       ###############################
        dbc.Col(dbc.Card([
        dbc.CardHeader("Min Humidity",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
        dbc.CardBody(
            [
                html.H4(id="load_minHumidity",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                    "text-align":"center","color":"#ffffff"},  className="card-title"),
                dcc.Interval(id='interval-minhum-component',n_intervals=270*1000,),
                #html.P("This is some card text", className="card-text"),
            ],
        ),
        dbc.CardFooter("(g.kg-1)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                            "text-align":"center","color":"#ffffff","font-weight":"bold",}),
    ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
   ), xs=6,sm=4,md=4,lg=2,xl=2,
   style = {"margin-top":"1%",}),
       
       

 ###########'padding-bottom':'10px'

         dbc.Col(dbc.Card([
         dbc.CardHeader("Min Temperature",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                             "text-align":"center","color":"#ffffff","font-weight":"bold",}),
         dbc.CardBody(
             [
                 html.H4(id="load_minTemperature", style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                                     "text-align":"center","color":"#ffffff"}, className="card-title"),
                 dcc.Interval(id='interval-mintemp-component',n_intervals=345*1000,),
                 #html.P("This is some card text", className="card-text"),
             ]
         ),
         dbc.CardFooter("(°C)",style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)",
                                             "text-align":"center","color":"#ffffff","font-weight":"bold",}),
     ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'height':'150px',},
     ), xs=6,sm=4,md=4,lg=2,xl=2,
     style = {"margin-top":"1%",})
       
            ],
            className="mb-4",
        ),
       
        style = {"background-color":"rgb(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)"}),
       
       #######################################################

       html.P(),
         dbc.Row(
            [
               
#########
html.P(),
        dbc.Col(
            dbc.Card(
                [
           
                   html.P(),
                    daq.Gauge(
                        id='Humidity-Gauge',
                        showCurrentValue=True,
                        scale={"start":0,"interval":20,"labelInterval":1},
                        color="#cb4154",
                        units="g.kg-1",
                        #value=avgHumidity,
                        label="Average Humidity",style = {"color":"#ffffff","font-weight":"bold","font-size":40,},
                        max=100,
                        min=0,
                        #style = {'backgroundColor': 'rgba(0,0,0,0.3)','display': 'block',}
                       
                        ),
                    dcc.Interval(id='interval-avghum-component',n_intervals=395*1000,),
                ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",'padding-bottom':'10px'},
       
                ),
          xs=12,sm=12,md=12,lg=3,xl=3
            ),
       
dbc.Col(dbc.Card([dcc.Graph(id='load-hum-graph',figure=fighum),dcc.Interval(id='interval-humgraph-component',n_intervals=475*1000,) ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",},
               
), xs=12,sm=12,md=12,lg=9,xl=9,
style = {"margin-top":"1%",}),
       
            ],
            className="mb-4"
        ),
         
         ######################################################
       
        dbc.Row(
            [
#######
html.P(),
       
        dbc.Col(
            dbc.Card(
                [
               
                    html.P(),
                       
                    daq.Gauge(
                        id='Temperature-Gauge',
                        showCurrentValue=True,
                        scale={"start":0,"interval":5,"labelInterval":2},
                        color="#cb4154",
                        units="°C",
                        #value=avgTemp,
                        label='Average Temperature',style = {"color":"#ffffff","font-weight":"bold","font-size":40,},
                        max=40,
                        min=0,
                        #style_label = {'color': 'rgba(#ffffff)',}
                        ),
                    dcc.Interval(id='interval-avgtemp-component',n_intervals=530*1000,),
            ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",}
    ), xs=12,sm=12,md=12,lg=3,xl=3
    ),
           
           
dbc.Col(dbc.Card([dcc.Graph(id='load-temp-graph',figure=figtemp),dcc.Interval(id='interval-tempgraph-component',n_intervals=595*1000,) ],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",}
), xs=12,sm=12,md=12,lg=9,xl=9,
style = {"margin-top":"1%",}),
            ],
            className="mb-4",
        ),
       
        ########################################################
       
         dbc.Row(
            [
# #######
#html.P(),
dbc.Col(dbc.Card([
dash_table.DataTable(
                id='load-data-table',
                data=newDF.to_dict('records'),
                #id="load_omni_trxns_dist_pie",
                style_cell={
                    'backgroundColor': 'rgba(0,0,0,0.2)',
                    'color': '#fff',
                    'border': '0.01px solid #000',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'width': 'auto',
                    'textOverflow': 'ellipsis',
                    'font-family': 'Verdana, Tahoma, sans-serif',
                    'font-size': '11px',
                    'text-align': 'center',
                    'overflow-y': 'auto',
                    'padding-left': '2%',
                },
                style_table={
                    'overflowX': 'auto', 'margin-top': '2%', 'overflow-y': 'auto'},
                style_as_list_view=False,
                style_data_conditional=[ {

                                    "if": {"state": "selected"},

                                    "backgroundColor": "inherit !important",

                                    "border": "inherit !important",

                                        }

                                    ],
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0.5)', 'font-size': '12px', 'color': 'white',
                    'text-align': 'left',
                    'border': '0.01px solid rgba(0,0,0,0.4)',
                    #'width': 'auto',
                    'font-weight':'bold',},
                sort_action='native',
                page_action='native',   # all data is passed to the table up-front
                page_size=6,
            ),dcc.Interval(id='interval-datatable-component',n_intervals=670*1000,)],style = {"background-color":"rgba(0,0,0,0.3)","border-color":"#cb4154",}
    ), xs=12,sm=12,md=12,lg=12,xl=12),

# dbc.Col(dcc.Graph(figure=figtemp), width=3)

           ],
            className="mb-4",
         ),
       html.P(),
       
       html.P(["℗ Powered by Drocon Infographics"], className = 'flicker2'),
        #########################################################
       html.H4("info@droconinfographics.com"
               ,style = {"background-color":"rgba(0,0,0,0.0)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#cb4154",}
               ),
       
    ]
)
    ]
    , style = {"background-color":"#b0e0e6","border-color":"#cb4154",})

@app.callback(
    Output('load_maxHumidity', 'children'),
    [Input('interval-mhum-component', 'n_intervals'), ])
def fn_maxHumidity(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    maxHumidity = df["Humidity"].max()
    return (maxHumidity)    
########################################
@app.callback(
    Output('load_Noreads', 'children'),
    [Input('interval-read-component', 'n_intervals'), ])
def fn_noreads(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    NoReads = df["pk"].count()
    return (NoReads)
########################################
@app.callback(
    Output('load_minHumidity', 'children'),
    [Input('interval-minhum-component', 'n_intervals'), ])
def fn_minHumidity(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    minHumidity = df["Humidity"].min()
    return (minHumidity)    
########################################    

@app.callback(
    Output('load_maxTemperature', 'children'),
    [Input('interval-maxtemp-component', 'n_intervals'), ])
def fn_maxTemperature(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    maxTemp = df["Temperature"].max()
    return (maxTemp)    
########################################

@app.callback(
    Output('load_minTemperature', 'children'),
    [Input('interval-mintemp-component', 'n_intervals'), ])
def fn_minTemperature(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    minTemp = df["Temperature"].min()
    return (minTemp)    
########################################

   
@app.callback(Output('Humidity-Gauge', 'value'),
              Input('interval-avghum-component', 'n_intervals'))
def update_output(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    value = round(df["Humidity"].mean(),2)
    return value

########################################
   
@app.callback(Output('Temperature-Gauge', 'value'),
              Input('interval-avgtemp-component', 'n_intervals'))
def update_tempoutput(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    value = round(df["Temperature"].mean(),2)
    return value

########################################
   
@app.callback(Output('load-hum-graph', 'figure'),
              Input('interval-humgraph-component', 'n_intervals'))
def update_humgraph(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    df = df.sort_values(by='time', ascending=True)
    fighum = px.area(df, x="time", y="Humidity",line_shape='spline',title='Humidity Hourly Trend',
                      labels={
                        "time": "Time of Day",
                        "Humidity": "Humidity (g.kg-1)"
                    }
                      , color_discrete_sequence=["#cb4154"],height=325
                      )
    fighum.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color':"#ffffff",
    'title_font_color':"#ffffff",
    "title_font":{'size': 20},
    })
    fighum.update_xaxes(showgrid=False)
    fighum.update_yaxes(showgrid=False)
    return fighum

########################################
   
@app.callback(Output('load-temp-graph', 'figure'),
              Input('interval-tempgraph-component', 'n_intervals'))
def update_tempgraph(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    df = df.sort_values(by='time', ascending=True)
    figtemp = px.area(df, x="time", y="Temperature",line_shape='spline',
                      title='Temperature Hourly Trend',
                      labels={
                         "time": "Time of Day",
                         "Temperature": "Temperature (°C)"
                     }
                      , color_discrete_sequence=["#cb4154"],height=325
                      )
    figtemp.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color':"#ffffff",
    'title_font_color':"#ffffff",
    "title_font":{'size': 20},
    })
    figtemp.update_xaxes(showgrid=False)
    figtemp.update_yaxes(showgrid=False)
    return figtemp

########################################
   
@app.callback(Output('load-data-table', 'data'),
              Input('interval-datatable-component', 'n_intervals'))
def update_datatable(n_intervals):
    df = pd.DataFrame()
    p = rc.pipeline()
    for key in rc.keys():
        p.hgetall(key)
    df = df.append(p.execute())
    df['time'] = pd.to_datetime(df['time'])
    df['Humidity'] = df['Humidity'].astype(int)
    df['Temperature'] = df['Temperature'].astype(int)
    df = df.sort_values(by='time', ascending=False)
    newDF = df.copy()
    newDF = newDF.rename(columns = {'pk':'event_id', 'time':'event_time', 'Humidity':'Humidity(g.kg-1)',
                          'Temperature':'Temperature(°C)'}, inplace = False)
    newdf2 = newDF.to_dict('records')
    return (newdf2)

if __name__ == '__main__':
    app.run_server(debug=True)
    
