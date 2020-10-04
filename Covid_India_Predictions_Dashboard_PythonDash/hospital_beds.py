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


#load hosp data
df_test = pd.read_csv('data/state_daily_hosp_resources.csv', index_col=0, parse_dates=True)
#df_test.index = pd.to_datetime(df_test['Date'])


# Initialize the app
#app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True



def get_options1(list_states1):
    dict_list1 = []
    for i in list_states1:
        dict_list1.append({'label': i, 'value': i})

    return dict_list1

def Resources():
    layout = html.Div(
        children=[nav,
#testing html div

html.Div(className='row',
         children=[
            html.Div(className='eight columns div-user-controls',
                     children=[
                         html.H2('HOSPITAL RESOURCE UTILIZATION BASED ON NUMBER OF INFECTED INDIVIDUALS',
                         style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25}),
                         html.P('Based on Markov Chain Monte Carlo we calculate the hospital resource requiremnts. 5 States are modelled namely:Maharashtra, Gujrat, Delhi, Madhya Pradesh and Karnataka. Same model can be applied to other States and UTs also.',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 18}),
                         html.P('Inputs: Confirmed Cases daily (Time series)',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 15}),
                         html.P('Outputs: Hospital Beds, ICUs, Ventilators',style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 15}),
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
                        ],style={'color': '#2031DF'}
                     ),
            html.Div(className='div-for-charts1',
                     children=[
                         dcc.Graph(id='timeseries6', config={'displayModeBar': False}, animate=True),

                     ],style={'backgroundColor': '#43EFDE'})
                      ])



        ],style={'backgroundColor': '#14EBD6'}

)
    return layout



# Callback for timeseries tested
@app.callback(Output('timeseries6', 'figure'),
              [Input('state1selector', 'value')])

def update_graph(selected_dropdown_value):
    trace1 = []
    trace2=[]
    trace3=[]
    df_sub = df_test
    state=selected_dropdown_value
    #for state in selected_dropdown_value:
    #print(state)
    trace1.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['Beds'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='Hospital Beds',
                                             textposition='bottom center'))
    trace2.append(go.Scatter(x=df_sub[df_sub['State'] ==state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['ICUs'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='ICUs',
                                             textposition='bottom center'))
    trace3.append(go.Scatter(x=df_sub[df_sub['State'] == state]['Date'],
                                             y=df_sub[df_sub['State'] == state]['Ventilators'],
                                             mode='lines',
                                             opacity=0.7,
                                             name='Ventilators',
                                             textposition='bottom center'))



    traces = [trace1,trace2,trace3]
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
                  title={'text': 'Hospital Resources', 'font': {'color': '#2031DF'}, 'x': 0.5},
                  xaxis={'color':'#2031DF'},
                  yaxis={'color':'#2031DF'},
                  font=dict(
                  family="sans-serif",
                  size=14,
                  color="#2031DF")
                  #legend={'color':'#2031DF'}

              ),

              }

    return figure




#if __name__ == '__main__':
#    app.run_server(debug=True)
