import dash_bootstrap_components as dbc
import dash_html_components as html


nba_logo = 'https://content.sportslogos.net/news/2017/07/New-NBA-Logo-1.png'
def create_navbar():
    navbar = dbc.NavbarSimple(children=[
        dbc.Row([
            dbc.Col(html.Img(src=nba_logo, height='20px')),
            dbc.Col(dbc.NavbarBrand(html.A('Home', href='/'), className='ml-2'))
        ],
            align='center',
            style={'position': 'absolute',
                   'left': '0',
                   'text-align': 'center',
                   'margin': 'auto'}),
        dbc.Row([
            dbc.Col(dbc.NavItem(dbc.NavLink('Visualizations', href='/viz')), className='ml-2',
                    style={'height': '37px'}),
            dbc.Col(dbc.NavItem(dbc.NavLink('Analytics', href='/analytics')), className='ml-2',
                    style={'height': '37px'})
        ],
            align='center',
            no_gutters=True
        )],
        color='dark',
        dark=True
    )

    return navbar