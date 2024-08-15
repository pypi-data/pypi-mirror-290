from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise   #for serving static files on Heroku

# Instantiate dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku)
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Your app title"

    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Hi. I'm your Dash app."""), html.Br()])

    # Body
    body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])

    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])

    # Assemble dash layout
    app.layout = html.Div([header, body, footer])

    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)



# from dash import Dash, html, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# external_scripts = [
#     {"src": "https://cdn.tailwindcss.com"}
# ]

# external_stylesheets = [
#     "https://rsms.me/inter/inter.css"
# ]

# app = Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

# app.layout = [
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ]

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

# def start() -> None:
#     print("Super califragilisticxpealodoshis")
#     app.run(debug=True)

# if __name__ == '__main__':
#     start()
