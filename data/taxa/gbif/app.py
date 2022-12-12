from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd

import json

app = Dash(__name__)

df = pd.read_csv('cleaned_occurrences.csv')

taxa_keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
gdf = df.groupby(taxa_keys).count()[['longitude']].rename({'longitude': 'occurrences'}, axis=1).reset_index()
gdf.head()

fig = px.sunburst(gdf, path=taxa_keys[:5], values='occurrences')

app.layout = html.Div(children=[
    html.Div(
        children=[
            dcc.Graph(
                id='taxa-sunburst',
                figure=fig,
                style={'width': '50%', 'float': 'left','margin': 'auto', 'height': '750px'}
            ),
            html.Div(
                id='iframe',
                style={'width': '50%', 'float': 'left','margin': 'auto', 'height': '750px'}
            )
        ]
    ),
    html.Pre(
        id='table',
        style={'overflowX': 'scroll', 'float': 'left','margin': 'auto'}
    ),
    html.Pre(
        id="click-info-output",
        style={'overflowX': 'scroll', 'float': 'left','margin': 'auto'}
    )
])

@app.callback(
    Output('click-info-output', 'children'),
    Input('taxa-sunburst', 'clickData')
)
def get_click_info(hover_data):
    return json.dumps(hover_data, indent=2)

@app.callback(
    Output('iframe', 'children'),
    Input('taxa-sunburst', 'clickData')
)
def update_iframe(click_data):
    if click_data:
        label = click_data['points'][0]['label']
        url = f'https://en.wikipedia.org/wiki/{label}'
        iframe = html.Iframe(
            src=url,
            style={'height': '100%', 'width': '100%'}
        )
        return iframe
    return ''

@app.callback(
    Output('table', 'children'),
    Input('taxa-sunburst', 'clickData')
)
def update_table(click_data):
    if click_data:
        _id = click_data['points'][0]['id']
        levels = _id.split('/')
        summary = gdf.copy()
        for i, level in enumerate(levels):
            summary = summary[summary[taxa_keys[i]] == level]
        summary = summary[taxa_keys].nunique().to_dict()
        return json.dumps(summary, indent=2)
    return ''

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
