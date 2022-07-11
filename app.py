import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc

index = pd.read_pickle('../../Dataset/indice_2022.pkl')
countries = pd.read_pickle('../../Dataset/paesi_2022.pkl')

fig = go.Figure()

for country in countries.index:
    df = index.stack('Year')['Components'].loc[country].T.stack().reset_index()
    #title = f"Components scores for {countries.loc[country, 'country_name']}"
    df.rename(columns={'Feature': 'Component',df.columns[2]:'Score'}, inplace=True)
    radar = px.line_polar(df, theta='Component', r='Score', line_close=True, line_group='Year', color='Year')
    fig.add_traces(radar.data[0])
    fig.add_traces(radar.data[1])


buttons = []
i = 0
for country in countries.index:
    args = [False] * 2*len(countries.index)
    args[i] = True
    args[i+1] = True
    button = dict(label = f"{countries.loc[country, 'Country name']}",
                  method = "update",
                  args=[{"visible": args}])
    buttons.append(button)
    i += 2
        
fig.update_layout(
    title="WeWorld Index 2022: Components Radar Chart",
    legend = dict(title='Year'),
    polar=dict(
            radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        angle=90, 
                        tickangle=90, #
            ),
            angularaxis = dict(
        #tickfont_size=8,
                        rotation=90, # start position of angular axis
                        direction="clockwise",
            )
    ),
    updatemenus=[dict(
                    active=0,
                    type="dropdown",
                    buttons=buttons,
                    x = 1,
                    y = 1.02,
                    xanchor = 'center',
                    yanchor = 'bottom',
    )], 
   # autosize=False,
   # width=1000,
   # height=800
)

app = Dash(__name__)
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
    app.run_server(debug=True, port=8051)