# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import redis

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
r = redis.Redis(host='192.168.121.189', port=6379, db=0, decode_responses=True)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    out = r.get('arthurlima-proj3-output')
    print(out)
