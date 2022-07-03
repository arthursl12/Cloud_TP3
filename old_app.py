# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import redis

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.subplots as psub
from plotly.graph_objects import Scatter
import plotly.express as px
import pandas as pd
from random import randrange

app = Dash(__name__)
r = redis.Redis(host='192.168.121.189', port=6379, db=0, decode_responses=True)

ts = {}
avgs = {}
STEP = 2
PRINT_LAST = 10

fig1 = psub.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
fig2 = psub.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
fig3 = psub.make_subplots(rows=1, cols=1, vertical_spacing=0.2)

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),

    html.Div(id="text", children='''
        Live monitoring dashboard with data from Redis
    '''),

    html.H2(id="60s-title", children='''
        CPU Usage - Last minute average
    '''),
    dcc.Graph(
        id='60s-graph',
        figure=fig1,
    ),
    html.H2(id="1h-title", children='''
        CPU Usage - Last hour average
    '''),
    dcc.Graph(
        id='1h-graph',
        figure=fig2
    ),
    html.H2(id="other-title", children='''
        Other graph
    '''),
    dcc.Graph(
        id='other-graph',
        figure=fig3
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])


def find_max_cpu_n(json_dict):
    keys = json_dict.keys()
    result_list = [i for i in keys if i.startswith("avg-util-cpu")]
    result = len(result_list) // 2
    return result

def allocate_dict(n_cpus):
    keys = ts.keys()
    for i in range(n_cpus):
        n = i+1
        if (f"avg-util-cpu{n}-60sec" not in keys):
            ts[f"avg-util-cpu{n}-60sec"] = []
        if (f"avg-util-cpu{n}-1h" not in keys):
            ts[f"avg-util-cpu{n}-1h"] = []
    if ("other-metric" not in keys):
        ts["other-metric"] = []
    
    keys = avgs.keys()
    for i in range(n_cpus):
        n = i+1
        if (f"avg-util-cpu{n}-60sec" not in keys):
            avgs[f"avg-util-cpu{n}-60sec"] = []
        if (f"avg-util-cpu{n}-1h" not in keys):
            avgs[f"avg-util-cpu{n}-1h"] = []
    if ("other-metric" not in keys):
        avgs["other-metric"] = []

def generate_titles(n_cpus, hour=False):
    titles = []
    for i in range(n_cpus):
        if (hour): titl = f"Average CPU {i+1} usage - last hour"
        else: titl = f"Average CPU {i+1} usage - last minute"
        titles.append(titl)
    return titles
    

@app.callback(
    [
        Output('60s-graph','figure'),
        Output('1h-graph','figure'),
        Output('other-graph','figure')
    ],
    Input('interval-component', 'n_intervals'))
def update_metrics(n):
    # print("Update called")
    
    # call redis, get a json
    redis_json = r.get('arthurlima-proj3-output')
    # redis_json = {
    #     "avg-util-cpu1-60sec": randrange(0,15),
    #     "avg-util-cpu2-60sec": randrange(0,15),
    #     "avg-util-cpu3-60sec": randrange(0,15),
    #     "avg-util-cpu4-60sec": randrange(0,15),
    #     "avg-util-cpu1-1h": randrange(0,15),
    #     "avg-util-cpu2-1h": randrange(0,15),
    #     "avg-util-cpu3-1h": randrange(0,15),
    #     "avg-util-cpu4-1h": randrange(0,15),
    #     "other-metric": randrange(15,20)
    # }
    n_cpus = find_max_cpu_n(redis_json)
    allocate_dict(n_cpus)
    
    
    # print(ts)
    # app.last_time += STEP
    # app.ts.append(app.last_time)
    # app.avgs.append(randrange(0,15))
    
    app.last_time += STEP
    # Add averages to interal variables, generate 60s graph
    fig1 = psub.make_subplots(rows=n_cpus, cols=1,
                              shared_yaxes=True,y_title='%')
    fig1['layout']['margin'] = {
        'l': 50, 'r': 10, 'b':15, 't': 10
    }
    fig1.update_layout(height=150*n_cpus, width=900)
    fig1.update_xaxes(visible=False, showticklabels=False)
    
    for i in range(n_cpus):
        n = i+1
        key = f"avg-util-cpu{n}-60sec"
        ts[key].append(app.last_time)
        avgs[key].append(redis_json[key])
        ts[key] = ts[key][-PRINT_LAST:]
        avgs[key] = avgs[key][-PRINT_LAST:]
        fig1.add_trace(Scatter(x=ts[key], y=avgs[key], name=f"CPU {i+1}"), 
                       row=n, col=1)
        fig1['layout'][f'yaxis{i+1}']['title']='%'
    
    # Add averages to interal variables, generate 1h graph
    fig2 = psub.make_subplots(rows=n_cpus, cols=1, shared_yaxes=True)
    fig2['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 5, 't': 10
    }
    fig2.update_xaxes(visible=False, showticklabels=False)
    fig2.update_layout(height=150*n_cpus, width=900, yaxis_title="%")
    
    for i in range(n_cpus):
        n = i+1
        key = f"avg-util-cpu{n}-1h"
        ts[key].append(app.last_time)
        avgs[key].append(redis_json[key])
        ts[key] = ts[key][-PRINT_LAST:]
        avgs[key] = avgs[key][-PRINT_LAST:]
        fig2.add_trace(Scatter(x=ts[key], y=avgs[key], 
                               name=f"CPU {i+1}"), 
                       row=n, col=1)
        fig2['layout'][f'yaxis{i+1}']['title']='%'
    
    # Generate other metric graph
    key = "other-metric"
    ts[key].append(app.last_time)
    avgs[key].append(redis_json[key])
    ts[key] = ts[key][-PRINT_LAST:]
    avgs[key] = avgs[key][-PRINT_LAST:]
    fig3 = px.line(x=ts[key], y=avgs[key])
    fig3.update_xaxes(visible=False, showticklabels=False)
    return fig1,fig2,fig3


if __name__ == '__main__':
    app.last_time = 0
    # app.ts = [0]
    # app.avgs = [0]
    app.run_server(debug=True)
    
    print(out)
