import plotly.express as px
import plotly.graph_objects as go
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import os 
import pandas as pd

csv_list = []
for files in os.listdir('data/'):
    csv_list.append(files)

combined_csv = pd.concat([pd.read_csv('data/' + f) for f in csv_list])
combined_csv.to_csv("combined.csv", index=False, encoding='utf-8-sig')
stats_columns = ['Field Goals', 'Field Goals Attempted',
                 'Field Goal Percentage', 'Three Pointers', 'Three Pointers Attempted',
                 'Three Point Percentage', 'Two Pointers', 'Two Pointers Attemped',
                 'Two Point Percentage', 'eFG%', 'Free Throws', 'Free Throws Attempted',
                 'Free Throw Percentage', 'Offensive Rebounds', 'Defensive Rebounds',
                 'Total Rebound', 'Assists', 'Steals', 'Blocks', 'Turnovers',
                 'Personal Fouls', 'Points']

server = flask.Flask(__name__)
app = dash.Dash(__name__, 
                server=server, 
                external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(children=[
    dbc.Alert(
        'You have entered an invalid player name, please try again',
        id='player_alert',
        dismissable=True,
        fade=True,
        is_open=False,
        color='danger'
    ),

    html.Br(),

    dbc.Input(id='text_input', placeholder='Enter a player name'),

    dbc.Select(
        id='stats_dropdown',
        options=[{'label': stat, 'value': stat} for stat in stats_columns]
    ),

    dcc.Graph(id='player_plot')
             # style=dict(display='flex', justifyContent='center'))
])

@app.callback(
    Output('player_alert', 'is_open'),
    [Input('text_input', 'value')],
    [State('player_alert', 'is_open')]
)
def toggle_player_alert(value, is_open):
    if str(value) not in list(combined_csv['Name'].values):
        return is_open
    return not is_open


@app.callback(
    Output('player_plot', 'figure'),
    [Input('text_input', 'value'),
     Input('stats_dropdown', 'value')]
)
def player_graph(text_input, stats_dropdown):
    filt_df = combined_csv[combined_csv['Name'] == text_input]
    stats = filt_df.loc[:, ['Season', str(stats_dropdown)]]
    return go.Figure([go.Scatter(x=stats['Season'], y=stats[stats_dropdown])])

if __name__ == '__main__':
    app.server.run(threaded=False)