import csv
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Inizialization connection with Firebase
cred = credentials.Certificate('certificate.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'url'
})

ref = db.reference('/')

#Update the Firebase data about umidity and lightning
def sendData(ill,umid):
    ref.update({
        'umidita' : int(umid),
        'illuminazione' : int(ill)
    })

#Take data from Thingspeak --> I'm gonna use them for the plots
newValue=[]

data = pd.read_csv('linkChannelThingSpeak',usecols=['created_at','field1','field2','field3','field4'])
for i in range(0,len(data.index),1):
    newValue.append(data.loc[i]['created_at'][0:19])

data = data.rename(columns={'created_at':'Date','field1':'umiditaTerreno','field2':'umiditaAmbiente','field3':'tempAmbiente','field4':'illAmbiente'})
data.Date = newValue


annotations=[]

fig = make_subplots(rows=2, cols=2) #Creates 2x2 subplots

fig.add_trace(go.Scatter(x = data['Date'], y = data['umiditaTerreno'],mode='lines+markers',line=dict(color='rgb(67,67,67)',width=1.2),marker=dict(size=5)),row=1,col=1) #Soil Moisture Plot

fig.add_trace(go.Scatter(x = data['Date'], y = data['umiditaAmbiente'],mode='lines+markers',line=dict(color='rgb(67,67,67)',width=1.2),marker=dict(size=5)),row=1,col=2) #Humidity Plot

fig.add_trace(go.Scatter(x = data['Date'], y = data['tempAmbiente'],mode='lines+markers',line=dict(color='rgb(67,67,67)',width=1.2),marker=dict(size=5)),row=2,col=1) #Temperature Plot

fig.add_trace(go.Scatter(x = data['Date'], y = data['illAmbiente'], mode='lines+markers', line=dict(color='rgb(67,67,67)',width=1.2),marker=dict(size=5)),row=2,col=2) #Lighting Plot

fig.update_xaxes(dict( #Update the xaxes of the first plot (1x1)
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),),row=1,col=1)

fig.update_xaxes(dict( #Update the xaxes of the seconds plot (1x2)
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),),row=1,col=2)

fig.update_xaxes(dict( #Update the xaxes of the third plot (2x1)
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),),row=2,col=1)

fig.update_xaxes(dict( #Update the xaxes of the fourth plot (2x2)
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),),row=2,col=2)

fig.update_yaxes(dict( #Update the xaxes of the first plot (1x1)
        showgrid=False,
        showline=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),row=1,col=1)

fig.update_yaxes(dict( #Update the xaxes of the seconds plot (1x2)
        showgrid=False,
        showline=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),row=1,col=2)

fig.update_yaxes(dict( #Update the xaxes of the third plot (2x1)
        showgrid=False,
        showline=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),row=2,col=1)

fig.update_yaxes(dict( #Update the xaxes of the fourth plot (2x2)
        showgrid=False,
        showline=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),row=2,col=2)

fig.update_layout( #Update the layout of all the plots
    autosize = True,
    height = 900,
    margin=dict(
        autoexpand=False,
        l=100,
        r=30
    ),
    showlegend=False,
    plot_bgcolor='white',
    title={
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
        },
)

#Adding annotations for 'fig'
fig.add_annotation({'font': {'size': 26,'color':'black'},
                     'showarrow': False,
                     'text': 'Umidità del Terreno',
                     'x': 0.225,
                     'xanchor': 'center',
                     'xref': 'paper',
                     'y': 1.0,
                     'yanchor': 'bottom',
                     'yref': 'paper'});

fig.add_annotation({'font': {'size': 26,'color':'black'},
                     'showarrow': False,
                     'text': 'Umidità Ambientale',
                     'x': 0.775,
                     'xanchor': 'center',
                     'xref': 'paper',
                     'y': 1.0,
                     'yanchor': 'bottom',
                     'yref': 'paper'});

fig.add_annotation({'font': {'size': 26,'color':'black'},
                     'showarrow': False,
                     'text': 'Temperatura',
                     'x': 0.225,
                     'xanchor': 'center',
                     'xref': 'paper',
                     'y': 0.425,
                     'yanchor': 'bottom',
                     'yref': 'paper'});

fig.add_annotation({'font': {'size': 26,'color':'black'},
                     'showarrow': False,
                     'text': 'Illuminazione Ambientale',
                     'x': 0.775,
                     'xanchor': 'center',
                     'xref': 'paper',
                     'y': 0.425,
                     'yanchor': 'bottom',
                     'yref': 'paper'});

plantsArray=[]
defaultPlant=""
illDefault=0
umidDefault=0
with open("plants.csv",'r',encoding="utf-8") as f:
    reader = csv.reader(f)
    counter=0
    pos=0
    for plant in reader:
        if(plant[1].upper()!="ILLUMINAZIONE"):
            counter+=1
            plantsArray.append(plant[0].upper())
            if(pos==counter):
                defaultPlant=plant[0].upper()
                illDefault=plant[1]
                umidDefault=plant[2]
        else:
            pos=int(plant[3])
    
app = Dash(__name__)

app.title='Irrigatore Automatico'

app.layout = html.Div([
    html.Div([
        html.H1(children='IRRIGATORE AUTOMATICO', style={'textAlign':'center','font-family':'Rockwell'}),
        html.Img(src='/assets/favicon.ico',style={'padding-left':'0.6%','height':'3em'}),
        ],style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    html.Div(
        children=[
            html.Div([
                dcc.Dropdown(plantsArray,defaultPlant,id="plants",clearable=False,style={'margin-top':'70%','width':'25vh','padding-left':'24%','text-align':'center','border-radius': '5px','font-family':'Rockwell'}),
                html.Br(),
                html.Div([
                    html.P("Umidità",style={'float':'center','font-family': 'Rockwell'}),
                    dcc.Input(illDefault,id="umidity", type="number", min=0,max=1024,style={
                        'padding': '10px',
                        'margin-left':'2%',
                        'width':'7vh',
                        'text-align':'center',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                        'background-color': '#f8f8f8'
                    }),
                ],style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Div([
                    html.P("Illuminazione",style={'float':'center','font-family': 'Rockwell'}),
                    dcc.Input(umidDefault,id="lightning", type="number", min=0,max=1024,style={
                        'padding': '10px',
                        'margin-left':'2%',
                        'width':'7vh',
                        'text-align':'center',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                        'background-color': '#f8f8f8'
                    }),
                ],style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Button("UPDATE", id="upload",style={
                    'background': 'linear-gradient(to bottom, #4c4c4c, #2c2c2c)',
                    'border-radius': '5px',
                    'color': 'white',
                    'padding': '10px 20px',
                    'box-shadow': '2px 2px 5px #888888',
                    'border': 'none',
                    'margin-top':'2%',
                    'font-family': 'Rockwell',
                    'font-size':16,
                }),
                html.P(id="placeholder"),
                ],
            style={'float':'left','vertical-align': 'middle','text-align':'center','width' : '24%', 'height':'70vh','display': 'inline-block'}),
            html.Div(
                dcc.Graph(figure=fig,config={"displayModeBar": False,"staticPlot":True}),
            style={'float':'left','width' : '76%', 'height':'50%','display': 'inline-block'}),
        ], style={'width' : '100%', 'display' : 'inline-block','height':'70vh'}),
])

#Update theCSV file that cointains the last data about each plant
def updateCSV(plantUp,ill,umid):
    pos=0
    for elemento in plantsArray:
        pos+=1
        if(plantUp.upper()==elemento.upper()):
            break;
    header=['pianta','illuminazione','umidita',pos]
    data=[]
    with open("plants.csv",'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        for plant in reader:
            if(plant[1].upper()!="ILLUMINAZIONE"):
                if(plant[0].upper()==plantUp):
                    data.append([plantUp,ill,umid])
                else:
                    data.append([plant[0],plant[1],plant[2]])
                    
    with open('plants.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
        
@app.callback(
    Output("placeholder","children"),
    State("umidity","value"),
    State("lightning","value"),
    State("plants","value"),
    Input("upload","n_clicks"),
)
def updateData(umidity,lightning,plant,clicks): #Call updateCSV() and sendData()
    if clicks is not None:
        updateCSV(plant,lightning,umidity)
        sendData(lightning,umidity)
        return ""

@app.callback(
    Output("lightning","value"),
    Input("plants","value"),
)
def setLightning(plants): #Set new illumination in the CSV file
    with open("plants.csv",'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        for plant in reader:
            if(plant[1].upper()!="ILLUMINAZIONE"):
                if(plant[0].upper()==plants):
                    return plant[1]

@app.callback(
    Output("umidity","value"),
    Input("plants","value"),
)
def setUmidity(plants): #Set new umidity in the CSV file
    with open("plants.csv",'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        for plant in reader:
            if(plant[1].upper()!="ILLUMINAZIONE"):
                if(plant[0].upper()==plants):
                    return plant[2]

if __name__ == '__main__':
    app.run_server(port=9000)
