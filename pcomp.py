import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

from viz import combined_csv, col_names, stats_columns
from navbar import create_navbar

navbar = create_navbar()

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app_layout = html.Div(children=[
    dbc.Col([
        html.Div(children=[
                dbc.Input(id='comp1_input', placeholder='Enter a player name'),
                html.Button(id='comp1_button', n_clicks=0, children='Submit'),
                dcc.Graph(
                    id='player1_plot'
                )
            ]
        ),
    ]),
    dbc.Col(dbc.Select(
                    id='comp_dropdown',
                    options=[{'label': stat, 'value': stat} for stat in stats_columns]
                )),
    dbc.Col(
        html.Div(children=[
                dbc.Input(id='comp2_input', placeholder='Enter a player name'),
                html.Button(id='comp2-button', n_clicks=0, children='Submit'),
                dcc.Graph(
                    id='player2_plot'
                )
            ])
    )
])


def create_pcomp():
    layout = html.Div([
        navbar,
        app_layout
    ])

    return layout


app.layout = create_pcomp()


if __name__ == '__main__':
    app.server.run(threaded=False)