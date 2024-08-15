

import argparse
from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__,external_stylesheets=external_stylesheets,pages_folder='pages',)

server = app.server

app.layout = html.Div([
    html.H1('Welcome to TradeStream'),
    html.h3('Select a task to run:'),
    dcc.Dropdown(['RUN_ALL', 'START_TRADING', 'START_STREAMING', 'NOTIFY_ONLY'],
        'RUN_ALL',
        id='dropdown'
    ),
    html.Div(id='display-value')
])

@callback(Output('display-value', 'children'), Input('dropdown', 'value'))
def display_value(value):
    return f'Task {value} started successfully!'


def start_app_server(debug:bool = False, run_local:bool = False):
    print("Starting dashboard app server")
    debug = False
    if argparse.argv[1] == "debug":
        print("Debug mode enabled for dashboard app server")
        debug = True
    app.run(debug=debug,run_local=run_local)

def start_app_server_debug():
    start_app_server(True,False)

if __name__ == '__main__':
    start_app_server(False,False)
