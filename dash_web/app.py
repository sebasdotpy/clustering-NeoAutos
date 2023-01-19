from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from waitress import serve

df = pd.read_csv('../data_clean.csv')

app = Dash(__name__)
app.title = 'Clusterización'

server = app.server

app.layout = html.Div([
    html.H1(children='Clusterización'),
    html.H4(children='Este es el ultimo cambio que hice'),
    dcc.Graph(id='bar-plot',
              figure=px.bar(df, y='price', x='Marca', color='Combustible', title='Bar plot: price vs Marca'),),
    dcc.Graph(id='box-plot',
              figure=px.histogram(df, x='Marca')),
    dcc.Graph(id='hist-price',
              figure=px.histogram(df, x='price', nbins=50))
])

if __name__=='__main__':
    # app.run_server(debug=True)
    serve(server, port=8050)