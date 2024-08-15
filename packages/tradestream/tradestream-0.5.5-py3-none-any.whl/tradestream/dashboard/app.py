

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

external_scripts = [
    {"src": "https://cdn.tailwindcss.com"}
]

external_stylesheets = [
    "https://rsms.me/inter/inter.css"
]

app = Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

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
