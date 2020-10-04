import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from covid_trends import Trends
from covid_death_predictions import Predictions
from homepage import Homepage
from hospital_beds import Resources
from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/time-series1':
        return Predictions()
    elif pathname == '/time-series':
        return Trends()
    elif pathname == '/time-series2':
        return Resources()
    else:
        return Homepage()


if __name__ == '__main__':
    app.run_server(debug=True)
