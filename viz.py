import plotly.graph_objects as go
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

import os 
import pandas as pd
import Levenshtein as lv

from navbar import create_navbar

navbar = create_navbar()

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

csv_list = []
for files in os.listdir('data/'):
    csv_list.append(files)

combined_csv = pd.concat([pd.read_csv('data/' + f) for f in csv_list])
combined_csv.to_csv("combined.csv", index=False, encoding='utf-8-sig')
col_names = ['Position', 'Age', 'Season', 'Team', 'Games', 'Games Started', 'Minutes Played',
             'Field Goals', 'Field Goals Attempted', 'Field Goal Percentage', 'Three Pointers',
             'Three Pointers Attempted', 'Three Point Percentage', 'Two Pointers', 'Two Pointers Attemped',
             'Two Point Percentage', 'eFG%', 'Free Throws', 'Free Throws Attempted', 'Free Throw Percentage',
             'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebound', 'Assists',
             'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points', 'MVP', 'ROY', 'PPG_leader', 'RPG_leader',
             'APG_leader', 'WS_leader']

stats_columns = ['Points', 'Field Goals', 'Field Goals Attempted',
                 'Field Goal Percentage', 'Three Pointers', 'Three Pointers Attempted',
                 'Three Point Percentage', 'Two Pointers', 'Two Pointers Attemped',
                 'Two Point Percentage', 'eFG%', 'Free Throws', 'Free Throws Attempted',
                 'Free Throw Percentage', 'Offensive Rebounds', 'Defensive Rebounds',
                 'Total Rebound', 'Assists', 'Steals', 'Blocks', 'Turnovers',
                 'Personal Fouls']

app_layout = html.Div(children=[
    html.Div([
        dbc.Input(id='text_input', placeholder='Enter a player name'),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        dbc.Select(
            id='stats_dropdown',
            options=[{'label': stat, 'value': stat} for stat in stats_columns]
        )]
    ),

    html.Br(),

    dash_table.DataTable(
        id='player_stats',
        columns=[{'name': i, 'id': i} for i in (col_names)],
        style_table={'overflowX': 'scroll'}
    ),

    html.Br(),

    dcc.Graph(
        id='player_plot'
    )
    # style=dict(display='flex', justifyContent='center'))
])


def create_app():
    layout = html.Div([
        navbar,
        app_layout
    ])

    return layout

app.layout = create_app()


if __name__ == '__main__':
    app.server.run(threaded=False)
