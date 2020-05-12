import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import requests

client_id = "mha9q6nzmn0q43oc0mmqzukfcgmkfq"
headers = {'Client-ID': client_id}
games_url = 'https://api.twitch.tv/helix/games'
streams_url = 'https://api.twitch.tv/helix/streams'
 
app = dash.Dash(__name__)
 
app.layout = html.Div(style={'backgroundColor': '#4b367b', 'padding': 30}, children=[
    html.H1(
        children='Top Twitch Streams',
        style={'textAlign': 'center'}
    ),
 
    html.Div(
        children='Select a Game and Number of Top Streams',
        style={'textAlign': 'center', 'fontSize': 20}
    ),
 
    html.Label('Game', style={'fontSize': 20}),
    dcc.Input(id='game_name', value='Counter-Strike: Global Offensive', type='text'),
 
    html.Label('Streams', style={'fontSize': 20, 'marginTop': 30}),
    dcc.Slider(
        id='stream_num',
        min=5,
        max=50,
        marks={i*5: str(i*5) for i in range(1, 11)},
        value=10,
    ),
 
    dcc.Graph(id='jobs_barchart', style={'marginTop': 30, 'marginBottom': 30}),
 
    html.Button(id='submit-button', n_clicks=0, children='Go',
        style={
            'display': 'block',
            'margin': 'auto',
            'width': 100,
            'textAlign': 'center',
            'fontSize': 20,
            'fontFamily': 'inherit',
            'color': '#00ff7f',
            'border-color': '#00ff7f',
            'border-width': 2,
        }
    ),
])
 
@app.callback(
    Output(component_id='jobs_barchart', component_property='figure'),
    [Input(component_id='submit-button', component_property='n_clicks'),],
    [State(component_id='game_name', component_property='value'),
     State(component_id='stream_num', component_property='value'),],
)
def update_figure(n_clicks, game, n_streams):
    if game == '':
        payload = {'first': n_streams}
        r = requests.get(streams_url, headers=headers, params=payload).json()
    else:
        payload = {'name': game}
        r = requests.get(games_url, headers=headers, params=payload).json()
        game_id = r['data'][0]['id']
        payload = {'game_id': game_id, 'first': n_streams}
        r = requests.get(streams_url, headers=headers, params=payload).json()
 
    return {
        'data': [
            go.Bar(
                x=[d['user_name']],
                y=[d['viewer_count']],
                text=d['title'],
                opacity=0.8,
                name=d['user_name'],
                hoverinfo='x+y+text',
                showlegend=False
            ) for d in r['data']
        ],
        'layout': go.Layout(
            xaxis={'title': 'Streams'},
            yaxis={'title': 'Viewers'},
            hovermode='closest',
            title = game + ' Streams with Most Current Viewers',
        )
    }
 
if __name__ == '__main__':
    app.run_server(debug=True)