import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from navbar import create_navbar


def homepage_layout():
    landing_page_layout = dbc.Jumbotron([
        html.H1('NBA Viz Tool', className='display-3'),
        html.P(children=[
            'NBA Visualization tool using data from ',
            html.A('Basketball Reference', href='https://www.basketball-reference.com')],
            className='lead'),
        html.P(children=[
            'Developed by Alexander Ilyin: ',
            html.A('Github Link', href='https://github.com/alexilyin1')],
            className='lead'),
        html.Hr(className='my-2'),
        html.P(
            dbc.Button('Press Here to Scrape',
                       id='scrape_button')
        ),
        html.Div(children=[
            dcc.Interval(id='progress-interval', n_intervals=59, interval=5),
            dbc.Progress(id='progress')
        ]),
        html.Hr(className='my-2'),
        html.P(children=[
            dbc.Button(html.A('Visualization Tools', href='/viz')),
            ' ',
            dbc.Button(html.A('Analytics Tools', href='/analytics'))
        ]),
        html.P(id='temp')
        ], fluid=True
    )

    return landing_page_layout


navbar = create_navbar()
body = homepage_layout()
def create_homepage():
    layout = html.Div([
        navbar,
        body
    ])

    return layout


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_homepage()

if __name__ == '__main__':
    app.server.run(threaded=False)