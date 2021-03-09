import pandas as pd
import os
import dash_core_components as dcc
from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import plotly
import numpy as np
import requests
import json
app = DjangoDash('PcqseNIcdBav8OJS')
app.title = 'P.Dashboard'
app.layout = html.Div(children=[
    html.H1(children='Application Sample'),
    html.Div(children='Plotly Dash App'),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Sydney'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Melbourne'},
            ],
            'layout': {
                'title': 'Data Graphs'
            }
        }
    )
])
