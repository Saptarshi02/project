import os
import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
from collections import deque



GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Manufacturing execution system"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Manufacturing Execution System", className="app__header__title"),
                        html.P(
                            "MES is a computerized systems used in manufacturing to track and document the transformation of raw materials to finished goods.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        # Machine Performance
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("Machine Performance", className="graph__title")]
                                ),
                                dcc.Dropdown(
                                    id = "dropdown_1",
                                    options=[
                                        {'label': i, 'value': i} for i in object
                                        #{'label': 'machine_02', 'value': 'machine_02'},
                                        #{'label': 'machine_03', 'value': 'machine_03'},
                                        #{'label': 'machine_04', 'value': 'machine_04'},
                                    ],
                                    value = 'machines',
                                    style = {"width": "50%"},
                                    #multi =True
                                )
                            ],
                            className='four columns'
                        ),
                        html.Div([        
                            dcc.Graph(
                                id="machine_performance",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor=app_color["graph_bg"],
                                        paper_bgcolor=app_color["graph_bg"],
                                    )
                                ),
                            ),
                        ], className='row'),
                    ],
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

@app.callback(
    Output("machine_performance", "figure"), 
    [Input("dropdown_1", "value")])
    
def update_graph(dropdown_name):
    conn = sqlite3.connect('D:/Mtech_Project/db/tutorial_1.db')
    df = pd.read_sql('SELECT object, value FROM tablevalue',conn)
    conn.close()
    dff=df[df['object']==dropdown_name]
    fig_1 = px.bar(dff, x='object', y='value')
    return fig_1



if __name__ == "__main__":
    app.run_server(port = 5895 , debug=True)