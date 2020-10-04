import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from app import app

from navbar import Navbar
nav = Navbar()

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

with open('./geojsons/india.geojson',encoding="utf8") as response:
     geojson_state = json.load(response)

latlong=  pd.read_csv('./data/latlong.csv',encoding= 'unicode_escape')
df_state = pd.read_csv('./data/state_wise.csv',dtype={"State": str})

#district
with open('./geojsons/Karnataka.geojson') as response:
     geojson_district = json.load(response)

df = pd.read_csv('./data/district_wise.csv',dtype={"District": str})
df_district = df[df['State']=='Karnataka']

fig_district = px.choropleth_mapbox(df_district, geojson=geojson_district, color="Confirmed",color_continuous_scale="oranges",
                           locations="District", featureidkey="properties.district",
                           center={"lat": 15.3173, "lon": 75.7139},
                           mapbox_style="carto-positron", zoom=5)
fig_district.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#state
fig_state = px.choropleth_mapbox(df_state, geojson=geojson_state, color="Confirmed",color_continuous_scale="oranges",
                           locations="State", featureidkey="properties.st_nm",
                           center={"lat": 20.5937, "lon": 78.9629},
                           mapbox_style="carto-positron", zoom=3)
fig_state.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

@app.callback(
    Output('district-map', 'figure'),
    [Input('state-map', 'hoverData')])

def callback_graph1(hoverData):
        #district
            if hoverData is None:
                v_index='Karnataka'
            else:
                v_index = hoverData['points'][0]['location']

            v_index=str(v_index)
            s_index = latlong[latlong['State']==v_index].index.values
            lat=float(latlong.loc[latlong['State'] == v_index, 'lat'].iloc[0])
            lon=float(latlong.loc[latlong['State'] == v_index, 'lon'].iloc[0])
            path="./geojsons/"+v_index+".geojson"

            with open(path) as response:
                geojson_district = json.load(response)

            df = pd.read_csv('./data/district_wise.csv',dtype={"District": str})
            df_district = df[df['State']==v_index]

            fig_district = px.choropleth_mapbox(df_district, geojson=geojson_district, color="Confirmed",color_continuous_scale="oranges",
                                      locations="District", featureidkey="properties.district",
                                      center={"lat": lat,"lon": lon},
                                      mapbox_style="carto-positron", zoom=5)
            fig_district.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            return fig_district

india_confirmed = df_state[df_state['State'] == 'India']['Confirmed']
india_confirmed_delta= df_state[df_state['State'] == 'India']['Delta_Confirmed']
india_active = df_state[df_state['State'] == 'India']['Active']
india_recovered = df_state[df_state['State'] == 'India']['Recovered']
india_recovered_delta = df_state[df_state['State'] == 'India']['Delta_Recovered']
india_deceased = df_state[df_state['State'] == 'India']['Deaths']
india_deceased_delta = df_state[df_state['State'] == 'India']['Delta_Deaths']

state_confirmed = df_state[df_state['State'] == 'Karnataka']['Confirmed']
state_active = df_state[df_state['State'] == 'Karnataka']['Active']
state_recovered = df_state[df_state['State'] == 'Karnataka']['Recovered']
state_deceased = df_state[df_state['State'] == 'Karnataka']['Deaths']

@app.callback(
    [Output('st_c',"children" ),
    Output('st_a',"children" ),
    Output('st_r',"children" ),
    Output('st_d',"children" )],
    [Input('state-map', 'hoverData')])

def callback_graph2(hoverData):
        #district
        if hoverData is None:
            v_index='Karnataka'
        else:
            v_index = hoverData['points'][0]['location']

        v_index=str(v_index)
        state_confirmed = df_state[df_state['State'] == v_index]['Confirmed']
        state_active = df_state[df_state['State'] == v_index]['Active']
        state_recovered = df_state[df_state['State'] == v_index]['Recovered']
        state_deceased = df_state[df_state['State'] == v_index]['Deaths']
        return state_confirmed,state_active,state_recovered,state_deceased

body = html.Div([
    html.H1("COVID INDIA DASHBOARD",style={
        'textAlign': 'center',
        'height' :'75px',
        'font-size':'50px',
        'color': '#ffffff'
    })

    #cards
            ,dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Confirmed",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(india_confirmed,style={'font-size':'20px'})
                    ]),
            ], color="danger", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Active",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(india_active,style={'font-size':'20px'})
                    ])
            ], color="warning", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Recovered",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(india_recovered,style={'font-size':'20px'})
                    ])
            ], color="success", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Deceased",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(india_deceased,style={'font-size':'20px'})
                    ])
            ], color="dark", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            #state data

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Confirmed",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(id='st_c',children=state_confirmed,style={'font-size':'20px'}),
                    ])
            ], color="danger", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Active",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(id='st_a',children=state_active,style={'font-size':'20px'}),
                    ])
            ], color="warning", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Recovered",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(id='st_r',children=state_recovered,style={'font-size':'20px'}),
                    ])
            ], color="success", inverse=True,style={"height": "10rem",'textAlign':'center'}))

            ,dbc.Col(dbc.Card([
                dbc.CardHeader([html.H4("Deceased",style={'height':'10px','font-size':'20px'})]),
                dbc.CardBody([
                        html.P(id='st_d',children=state_deceased,style={'font-size':'20px'}),
                    ])
            ], color="dark", inverse=True,style={"height": "10rem",'textAlign':'center'}))


#maps
            ])
        ,dbc.Row([
                dbc.Col(html.Div([   # this Div contains india map\\\\\\\\\\\\\\\\\
                dcc.Graph(id='state-map',
                    figure=fig_state
                )], style={'width':'100%','height':'100%','display':'inline-block'}))
                , dbc.Col(html.Div([  # this Div contains state map
                dcc.Graph(id='district-map',
                    figure=fig_district
                )], style={'width':'100%', 'height':'100%','display':'inline-block'}))
                ])
        ])

def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

#app.layout = html.Div([body])

#if __name__ == "__main__":
    #app.run_server(debug = True)
