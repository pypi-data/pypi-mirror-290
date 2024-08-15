

import argparse
from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1('Hello World'),
    dcc.Dropdown(['LA', 'NYC', 'MTL'],
        'LA',
        id='dropdown'
    ),
    html.Div(id='display-value')
])

@callback(Output('display-value', 'children'), Input('dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    print("Starting dashboard app server")
    debug = False
    if argparse.argv[1] == "debug":
        print("Debug mode enabled for dashboard app server")
        debug = True
    app.run(debug=debug,dev_tools_hot_reload=True,host=os.environ["WEB_HOST"],port=os.environ["WEB_PORT"])
