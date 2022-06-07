#Import Dependancies
import dash_bootstrap_components as dbc
import dash
#Sfrom dash.dependencies import Input,Output
import dash_daq as daq
from dash import dcc,html,dash_table
import plotly.express as px
import redis
import pandas as pd
from datetime import timedelta, datetime as dt
#import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

   
df = pd.read_csv("data.csv")

# Transformations

# Eliminating test records
df = df.loc[(df['device'] == '1FA1A28')]

# Converting time, humidity and temperature into int
#df['time'] = df['time'].astype(int)   # Transform as numeric
df['time'] = pd.to_datetime(df['time'])
df['Humidity'] = df['Humidity'].astype(int)
df['Temperature'] = df['Temperature'].astype(int)
# check column data types
coltypes = df.dtypes
print(coltypes)

# Converting time from Epoch Unix to datetime
#df['time'] = pd.to_datetime(df['time'], unit='s', utc=False)
#df['time'] += timedelta(hours=3)

# Sorting data frame in descending order based on time
df = df.sort_values(by='time', ascending=False)

# getting aggrgates
avgTemp = round(df["Temperature"].mean(),2)
avgHumidity =  round(df["Humidity"].mean(),2)
minTemp = df["Temperature"].min()
maxTemp = df["Temperature"].max()
minHumidity = df["Humidity"].min()
maxHumidity = df["Humidity"].max()
NoReads = df["pk"].count()
print(NoReads)
Deviceid = df.iloc[0,2]
latestdate = str(df["time"].max())
latestTimestamp = dt.strptime(latestdate, '%Y-%m-%d %H:%M:%S')
latestTime = latestTimestamp.strftime('%H:%M:%S')

# visualizations

#plotting the gauge charts
#Humidity gauge chart
figtemp = px.area(df, x="time", y="Temperature",line_shape='spline',title='Temperature Hourly Trend'
                  , color_discrete_sequence=["#cb4154"],height=325)
fighum = px.area(df, x="time", y="Humidity",line_shape='spline',title='Humidity Hourly Trend'
                 , color_discrete_sequence=["#cb4154"],height=325)

app.layout = dbc.Container(fluid=True,
                            children=[
    html.Div(
    [

     html.P(),
     
     html.H4("DHT11 Temperature & Humidity Sensor Analytics"),
     html.P(),
     html.P(),
     dbc.Card(
        dbc.Row(
            [
##########
html.P(),

dbc.Col(dbc.Card([
        dbc.CardHeader("Device ID",style = {"background-color":"rgb(0,0,0,0.8)","border-color":"rgb(0,0,0,0.0)","text-align":"center","color":"#fff"}),
        dbc.CardBody(
            [
                html.H4(Deviceid, className="card-title"),
               # html.P("This is some card text", className="card-text"),
            ]
        ),
        #dbc.CardFooter("This is the footer"),
    ],
    ), width=2),

    dbc.Col(dbc.Card([
    dbc.CardHeader("Number of Hits"),
    dbc.CardBody(
        [
            html.H4(NoReads, className="card-title"),
           # html.P("This is some card text", className="card-text"),
        ]
    ),
    #dbc.CardFooter("This is the footer"),
],
), width=2),
       
        dbc.Col(dbc.Card([
        dbc.CardHeader("Maximum Humidity"),
        dbc.CardBody(
            [
                html.H4(maxHumidity, className="card-title"),
                #html.P("This is some card text", className="card-text"),
            ]
        ),
        #dbc.CardFooter("This is the footer"),
    ],
   ), width=2),
       
       
        dbc.Col(dbc.Card([
        dbc.CardHeader("Minimum Humidity"),
        dbc.CardBody(
            [
                html.H4(minHumidity, className="card-title"),
                #html.P("This is some card text", className="card-text"),
            ]
        ),
        #dbc.CardFooter("This is the footer"),
    ],
   ), width=2),
       
       
        dbc.Col(dbc.Card([
        dbc.CardHeader("Maximum Temperature"),
        dbc.CardBody(
            [
                html.H4(maxTemp, className="card-title"),
                #html.P("This is some card text", className="card-text"),
            ]
        ),
        #dbc.CardFooter("This is the footer"),
    ],
    ), width=2),
 ###########

         dbc.Col(dbc.Card([
         dbc.CardHeader("Minimum Temperature"),
         dbc.CardBody(
             [
                 html.H4(minTemp, className="card-title"),
                 #html.P("This is some card text", className="card-text"),
             ]
         ),
         #dbc.CardFooter("This is the footer"),
     ],
     ), width=2)
       
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
           
               
                daq.Gauge(
                id='Humidity-Gauge',
                showCurrentValue=True,
                scale={'start': 30, 'interval': 10, 'labelInterval': 20},
                #color={"gradient":True,"ranges":{"green":[10,19],"yellow":[20,26],"red":[27,30]}},
                units="g.kg-1",
                value=avgHumidity,
                label='Average Humidity',
                max=100,
                min=30,
                style = {"background-color":"rgb(0,0,0,0.6)","color":"#fff"}
        ), width=3
),
dbc.Col(dcc.Graph(figure=fighum), width=9)
       
            ],
            className="mb-4"
        ),
         
         ######################################################
       
        dbc.Row(
            [
#######
html.P(),
        dbc.Col(
        daq.Gauge(
            id='Temperature-Gauge',
            showCurrentValue=True,
            scale={'start': 10, 'interval': 3, 'labelInterval': 3},
            color={"gradient":True,"ranges":{"green":[10,19],"yellow":[20,26],"red":[27,30]}},
            units="°C",
            value=avgTemp,
            label='Average Temperature',
            max=30,
            min=10
            ), width=3
),
dbc.Col(dcc.Graph(figure=figtemp), width=9)
            ],
            className="mb-4",
        ),
       
        ########################################################
       
#         dbc.Row(
#             [
# #######
html.P(),

dash_table.DataTable(
                data=df.to_dict('records'),
                #id="load_omni_trxns_dist_pie",
                style_cell={
                    'backgroundColor': 'rgba(0,0,0,0.5)',
                    'color': '#fff',
                    'border': '0.01px solid #000',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'textOverflow': 'ellipsis',
                    'font-family': 'Verdana, Tahoma, sans-serif',
                    'font-size': '11px',
                    'text-align': 'left',
                    'overflow-y': 'auto',
                    'padding-left': '2%',
                },
                style_table={
                    'overflowX': 'auto', 'margin-top': '2%', 'overflow-y': 'auto'},
                style_as_list_view=False,
                style_header={
                    'backgroundColor': 'rgba(0,0,0,0.9)', 'font-size': '12px', 'color': 'grey', 'border': '0.01px solid rgba(0,0,0,0.4)', },
                sort_action='native',
                page_action='native',   # all data is passed to the table up-front
                page_size=15,
            ),

# dbc.Col(dcc.Graph(figure=figtemp), width=3)

#             ],
#             className="mb-4",
#         ),
#        html.P(),
        #########################################################
       
    ]
)
    ]
    , style = {"background-color":"#b0e0e6"})
# @app.callback(Output('Temperature-Gauge', 'value'))
# def update_output(value):
#     return value

if __name__ == '__main__':
    app.run_server(debug=True)
