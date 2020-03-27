import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import time
import os
import pandas as pd
import Levenshtein as lv
import plotly.graph_objects as go

from homepage import create_homepage
from viz import create_app
from watch import on_created, create_handler, create_observer

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

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

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-content')
])


@app.callback(
    [Output('progress', 'value'), Output('progress', 'children')],
    [Input('progress-interval', 'n_intervals'),
     Input('scrape_button', 'n_clicks')]
)
def update_progress(intervals, n):
    if n == 0:
        return 0, f'{0}%'
    else:
        for file in os.listdir('static/'):
            os.remove('static/' + file)

        handler = create_handler()
        observer = create_observer('static/', handler)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
        return 100, f'{100}%'


@app.callback(
    Output('temp', 'value'),
    [Input('scrape_button', 'n_clicks')]
)
def start_scrape(n):
    if n == 0:
        return 0
    return os.system('py scraper.py')


@app.callback(
    Output('player_stats', 'data'),
    [Input('submit-button', 'n_clicks')],
    [State('text_input', 'value')]
)
def stats_table(n_clicks, text):
    text = " ".join([str.capitalize() for str in text.split(' ')])
    filt_df = combined_csv[combined_csv['Name'] == text]
    if len(filt_df) > 0 and n_clicks:
        return filt_df.to_dict('rows')
    else:
        return ''


@app.callback(
    Output('player_plot', 'figure'),
    [Input('text_input', 'value'),
     Input('stats_dropdown', 'value')]
)
def player_graph(text_input, stats_dropdown):
    text_input = " ".join([str.capitalize() for str in text_input.split(' ')])
    filt_df = combined_csv[combined_csv['Name'] == text_input]
    stats = filt_df.loc[:, ['Season', str(stats_dropdown)]]
    if text_input in combined_csv['Name'].values:
        return go.Figure([go.Scatter(x=stats['Season'], y=stats[stats_dropdown])])
    elif text_input is None or len(stats)==0:
        lev_dict = {'Name': [],
                    'Score': []}
        for x in set(list(combined_csv['Name'].values)):
            lev_dict['Name'].append(x)
            lev_dict['Score'].append(lv.distance(text_input, x))
        lev_df = pd.DataFrame.from_dict(lev_dict)
        top = lev_df.sort_values('Score', ascending=True).iloc[0:5,]['Name'].values
        return {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "annotations": [
                        {
                            "text": "Player not Found, did you mean {}".format([Name for Name in top]),
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 10
                            }
                        }
                    ]
                }
            }


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/viz':
        return create_app()
    elif pathname == '/analytics':
        return ''
    elif pathname == '/':
        return create_homepage()


if __name__ == '__main__':
    app.server.run()