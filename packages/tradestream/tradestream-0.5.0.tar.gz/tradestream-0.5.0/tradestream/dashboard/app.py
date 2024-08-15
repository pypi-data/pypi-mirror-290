

# from dash import Dash, dcc, html, Input, Output, callback

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__,external_stylesheets=external_stylesheets,pages_folder='pages',)

# app.enable_pages = True
# app.enable_dev_tools = True

# server = app.server

# app.layout = html.Div([
#     html.H1('Welcome to TradeStream'),
#     html.h3('Select a task to run:'),
#     dcc.Dropdown(['RUN_ALL', 'START_TRADING', 'START_STREAMING', 'NOTIFY_ONLY'],
#         'RUN_ALL',
#         id='dropdown'
#     ),
#     html.Div(id='display-value')
# ])

# @callback(Output('display-value', 'children'), Input('dropdown', 'value'))

# def display_value(value):
#     return f'Task {value} started successfully!'

# def start(debug:bool = False, run_local:bool = False):
#     print("Starting dashboard app server")
#     app.run(debug=debug,run_local=run_local)

# def start_debug():
#     start(True,False)

# if __name__ == '__main__':
#     start(False,False)


from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

def start() -> None:
    print("Super califragilisticxpealodoshis")
    app.run(debug=True)

if __name__ == '__main__':
    start()
