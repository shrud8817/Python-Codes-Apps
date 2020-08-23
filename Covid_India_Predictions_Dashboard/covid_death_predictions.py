import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app

from navbar import Navbar
nav = Navbar()


# Load data
df = pd.read_csv('data/Death_Predictions.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'], format="%d-%b")
#print (df.index)

# Initialize the app
#app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config.suppress_callback_exceptions = True


def get_options(list_states):
    dict_list = []
    for i in list_states:
        dict_list.append({'label': i, 'value': i})
    return dict_list

def Predictions():
    layout = html.Div(
    children=[nav,
        html.Div(className='row',
                 children=[
                    html.Div(className='eight columns div-user-controls',
                             children=[
                                 html.H2('DEATH PREDICTION TRENDS',
                                 style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25}),
                                 html.P('Non linear mixed effects model with and locational variations in random effects.Data is modelled from available national and global sources up to current date. Predictions are made for a 14 day (2 week) interval. We have made state specific model optimization.5 States are modelled namely: Maharashtra, Gujrat, Delhi, Madhya Pradesh and Karnataka.  Same model can be applied to other States and UTs also.',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 18}),
                                 html.P('Inputs: Deaths daily (TIme series)',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 15}),
                                 html.P('Outputs:Log(Cumulative Death Rates)',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 15}),
                                 html.P('Inferences: Cumulative Death Rates, Daily Death Rates, Daily Deaths, Cumulative of Daily Deaths (All in TIme Series) ',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 15}),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stateselector', options=get_options(df['State'].unique()),
                                                      multi=True, value=[df['State'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stateselector'
                                                      )

                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='div-for-charts',
                             children=[
                                 dcc.Graph(id='timeseries4', config={'displayModeBar': False}, animate=True),
                                 dcc.Graph(id='timeseries5', config={'displayModeBar': False}, animate=True)

                             ],style={'backgroundColor': '#43EFDE','height':'100%'})
                              ])

        ],style={'backgroundColor': '#14EBD6','height':'100%'}

)
    return layout


# Callback for death rate
@app.callback(Output('timeseries4', 'figure'),
              [Input('stateselector', 'value')])

def update_graph1(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for state in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                 y=df_sub[df_sub['State'] == state]['Death rate'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=state,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#34c6cb", '#2ad56e', '#d56e2a', '#d12e3c', '#e21d7d', '#ccdb24'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  #plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Death Rate', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]}  ,
              ),

              }



    return figure

# Callback for timeseries deceased
@app.callback(Output('timeseries5', 'figure'),
              [Input('stateselector', 'value')])

def update_graph2(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for state in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                 y=df_sub[df_sub['State'] == state]['Cumulative death rate'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=state,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#34c6cb", '#2ad56e', '#d56e2a', '#d12e3c', '#e21d7d', '#ccdb24'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  #plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Cumulative Death Rate', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                 # xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure



#if __name__ == '__main__':
#    app.run_server(debug=True)
