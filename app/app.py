import os
import io
import sys
import dash
import plotly
import sqlite3
import dash_auth
import loremipsum
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State

from flask import send_from_directory
from loremipsum import get_sentences


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    ['queryshare_user', 'ETjKiz24']
]
app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.title = 'Query Share'
# app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True


# --------------------------- preprocessing ---------------------------


# load objects or other (To use it, like "processing.objname")
# conn = sqlite3.connect("iris_db.db")
# df_iris = pd.read_sql("select * from iris_test", conn)

# sql database
conn_sqldb = sqlite3.connect("data/sql_db.db")
df_sql_table = pd.read_sql("select * from sql_table", conn_sqldb)
c_user_id = 'AAA'
sql_table_current = df_sql_table.query('ID in "' + c_user_id + '"')

# --------------------------- define function -------------------------


# --------------------------- app_layout ---------------------------


# define resusable components ------------------------

# define title components (reusable components)
title_components = html.Div([

    # load local css
    # ------------- style -------------
    html.Link(rel='stylesheet', href='/static/sty.css'),
    html.Link(rel='stylesheet', href='/static/animate.css'),
    # ------------- font-family -------------
    html.Link(rel='stylesheet', href='/static/montserrat.css'),
    html.Link(rel='stylesheet', href='/static/notosans.css'),
    html.Link(rel='stylesheet', href='/static/Raleway.css'),



    # header div
    html.Div([
        html.Div([
            html.Div([
                html.Div(["Query Share"], id="header"),
                html.Div([dcc.Link('Write Query', href='/add_player', id='header-right')],
                         style={'cursor': 'pointer', 'float': 'right', 'margin-right': '7%'}),
                html.Div([dcc.Link('TOP', href='/', id='header-right')],
                         style={'cursor': 'pointer', 'float': 'right'})
            ]),
        ],id="header-bk", style={'font-family': 'Montserrat', 'width': '100%'}),
    ],id="header-fixed"),

    # title
    html.Div([
        # html.H1(['Query Share'], id='title_h')
        html.H1([''], id='title_h')
    ], style={'width': '100%', 'text-align':'center'})
])

# define footer conponents (reusable)
footer_components = html.Div([
    # footer div
    html.Div([
        html.Div([
            html.Div([html.A('©️Sasaki Kensuke ', href='https://qiita.com/sasaki_K_sasaki/items/6eb67a218c06dd56778e')], id="footer")
        ],id="footer-bk")
    ],id="footer-fixed")
])


# define toppage layout ------------------------

page_1_layout = html.Div([

    title_components,

    # html.Div([
    #     html.Div(
    #         html.H1("練習メニューを最適化します！")
    #         )
    # ], style={'width': '100%', 'text-align':'center'}),

    # dropdown div
    html.Div([

    html.Div([
        dcc.Tabs(
            tabs=[{'label': i, 'value': j} for i,j in zip(sql_table_current.Name,
                                                          sql_table_current.index.tolist())
            ],
            value=1,
            id='tabs',
            vertical=False
        ),
        html.Div(id='tab-output')
    ], style={
        'width': '100%',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'margin-bottom': '5%'
    }),



        footer_components

    ],
    style={'width': '100%', 'position': 'auto', 'margin': 'auto'}),

],
id='wrapper',
style={'position': 'relative', 'width': '100%', 'font-family': 'Noto Sans JP'})



@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    test_query=[statement for statement in sql_table_current.Statement],

    return html.Div([
        html.Br(),
        html.Div([
        dcc.Textarea(
            id="input_query",
            placeholder='Please write query',
            value=test_query[0][value-1],
            style={'width': '99%',
                   'display': 'table',
                   'position': 'auto',
                   'margin': 'auto',
                   'margin-left':'2px',
                   'height': "200px",
                   'font-family':'Monaco',
                   'font-size': "18px",
                   'border': 'solid 2px #5DC8BB',
                   'border-radius': '4px'
                   }

        )],style={'width' : '100%'}
        ),
        html.Div([
            html.Ul([
                html.Li(html.Button('RUN',
                                     id='button-run',
                                     className='square_btn')),
                html.Li(html.Button('SAVE',
                                     id='button-save',
                                     className='square_btn')),
            ], style={'list-style':'none',
                      'display': 'flex',
                      'justify-content': 'flex-end'})
        ]),
    # define table app_layout
    html.Div([
        dt.DataTable(
            rows=[{}], # initialise the rows
            # header_row_height="50px",
            enable_drag_and_drop=False,
            # min_width="100%",
            row_selectable=False,
            filterable=False,
            sortable=True,
            id='datatable'
        )], style={'width': '90%',
                   'height': '90%',
                   'position': 'auto',
                   'margin': 'auto',
                   'max-width':'1100px',
                   'margin-top': '24px',
                   'margin-bottom':'24px'}
    )
    ], style={
        'background-color': "white"
    })
@app.callback(Output('datatable', 'rows'),
              [Input('button-run', 'n_clicks')],
              [State('input_query', 'value')])
def execte_query(n_clicks, value):
    conn = sqlite3.connect("data/test_db.db")
    # define statement
    statement = value
    df_fromdb = pd.read_sql(statement, conn)
    return df_fromdb.to_dict('records')
    # table name is linnerud_test




















# define page2 layout ------------------------

input_style = { 'border':'0',
                'padding':'10px',
                'font-size':'1em',
                'font-family':'Arial, sans-serif',
                'color':'#aaa',
                'border':'solid 1px #ccc',
                'margin':'0 0 20px',
                'width':'100%',
                '-webkit-border-radius': '3px',
                '-moz-border-radius': '3px',
                'border-radius': '3px' }

page_2_layout = html.Div([

    title_components,

    html.Div([
        html.Div([
                html.H2("Please write your query name."),
                dcc.Input(id='input-box',
                          type='url',
                          placeholder='please write Article title ...',
                          style=input_style)
                  ],
                 style={'width': '100%'}),
        html.Button('Create', id='button', className='square_btn', style={'margin-bottom': '3%'}),
        html.Div(id='output-container-button',
                 children='Enter a value and press submit')
    ], style={'width': '100%', 'color': '#373939', 'font-style': 'Noto Sans JP' }),

    footer_components

],id='wrapper',
style={'position': 'relative', 'width': '100%', 'font-family': 'Noto Sans JP'})


@app.callback(Output('output-container-button', 'children'),
              [Input('button', 'n_clicks')],
              [State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'RESULT : "{}" CLICKED {} times'.format(
        value,
        n_clicks
    )

# define whole layout ------------------------

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    html.Div(id='page-content')
])


# --------------------------- app_table return logic ---------------------------


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_1_layout
    elif pathname == '/add_player':
        return page_2_layout
    # You could also return a 404 "URL not found" page here


# --------------------------- add stylesheet ---------------------------

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)



if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')
