import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from app import app

from navbar import Navbar
nav = Navbar()

# Load data
df = pd.read_csv('data/state_daily.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'], format="%d-%b")

#load testing data
df_test = pd.read_csv('data/state_daily_test.csv', index_col=0, parse_dates=True)
df_test.index = pd.to_datetime(df_test['Date'], format="%d-%b")


# Initialize the app
#app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True


def get_options(list_states):
    dict_list = []
    for i in list_states:
        dict_list.append({'label': i, 'value': i})

    return dict_list

def get_options1(list_states1):
    dict_list1 = []
    for i in list_states1:
        dict_list1.append({'label': i, 'value': i})

    return dict_list1

def Trends():
    layout = html.Div(
        children=[nav,
            html.Div(className='row',
                 children=[
                    html.Div(className='eight columns div-user-controls',
                             children=[
                                 html.H2('TREND FOR CONFIRMED, RECOVERED AND DECEASED CASES',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25}),
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
                                 dcc.Graph(id='timeseries',style={'height':'50vh'}, config={'displayModeBar': False}, animate=True),
                                 dcc.Graph(id='timeseries1',style={'height':'50vh'}, config={'displayModeBar': False}, animate=True),
                                 dcc.Graph(id='timeseries2',style={'height':'50vh'}, config={'displayModeBar': False}, animate=True)
                             ],style={'backgroundColor': '#43EFDE','height':'100%'})
                              ]),
#testing html div

html.Div(className='row',
         children=[
            html.Div(className='four columns div-user-controls',
                     children=[
                         html.H2('TREND FOR TESTING',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25}),
                         #html.P('Visualising time series with Plotly - Dash.'),
                         #html.P('Pick one or more testing metrics from the dropdown below.'),
                         html.Div(
                             className='div-for-dropdown',
                             children=[
                                 dcc.Dropdown(id='state1selector', options=get_options1(df_test['State'].unique()),
                                               multi=False, value='Delhi',
                                              style={'backgroundColor': '#1E1E1E'},
                                              className='state1selector'
                                              )

                             ],
                             style={'color': '#1E1E1E'})
                        ]
                     ),
            html.Div(className='div-for-charts1',
            #html.Div(className='div-for-charts',
                     children=[
                         dcc.Graph(id='timeseries3', config={'displayModeBar': False}, animate=True),

                     ],style={'backgroundColor': '#43EFDE','height':'100%'})
                      ])



        ],style={'backgroundColor': '#14EBD6','height':'100%'}

)
    return layout

# Callback for timeseries confirmed
@app.callback(Output('timeseries', 'figure'),
              [Input('stateselector', 'value')])

def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for state in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                 y=df_sub[df_sub['State'] == state]['Confirmed'],
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
                 # plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Confirmed Cases', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure

# Callback for timeseries deceased
@app.callback(Output('timeseries1', 'figure'),
              [Input('stateselector', 'value')])

def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for state in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                 y=df_sub[df_sub['State'] == state]['Deceased'],
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
                  title={'text': 'Deceased Cases', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure


# Callback for timeseries recovered
@app.callback(Output('timeseries2', 'figure'),
              [Input('stateselector', 'value')])

def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    #print(selected_dropdown_value)
    for state in selected_dropdown_value:
        #print(state)
        trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                 y=df_sub[df_sub['State'] == state]['Recovered'],
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
                  title={'text': 'Recovered Cases', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure

# Callback for timeseries tested
@app.callback(Output('timeseries3', 'figure'),
              [Input('state1selector', 'value')])

def update_graph(selected_dropdown_value):
    trace1 = []
    trace2=[]
    trace3=[]
    df_sub = df_test
    state=selected_dropdown_value
    #for state in selected_dropdown_value:
    print(state)
    trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['Tested'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='Tested',
                                             textposition='bottom center'))
    trace2.append(go.Scatter(x=df_sub[df_sub['State'] ==state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['Positive'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='Positive',
                                             textposition='bottom center'))
    trace3.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['Tests Per Million'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='Tests Per Million',
                                             textposition='bottom center'))



    traces = [trace1,trace2,trace3]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#34c6cb", '#2ad56e', '#d56e2a', '#d12e3c', '#e21d7d', '#ccdb24'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                 # plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Tested Cases', 'font': {'color': '#2031DF'}, 'x': 0.5},
                   xaxis={'color':'#2031DF'},
                   yaxis={'color':'#2031DF'},
                   font=dict(
                   family="sans-serif",
                   size=14,
                   color="#2031DF")
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure




#if __name__ == '__main__':
#    app.run_server(debug=True)
