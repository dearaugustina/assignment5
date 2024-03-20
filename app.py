# import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Load the dataset
df = pd.read_csv('gdp_pcap.csv')

# extract unique countries for dropdown options
countries = df['country'].unique()

# determine the range of years for the slider
years = [int(year) for year in df.columns[1:]]  # Convert year columns to integers

# Initialize the Dash app
app = Dash(__name__)
app.title = 'GDP Per Capita Analysis'
server = app.server





app.layout = html.Div([
    html.H1('GDP Per Capita Analysis', style={'textAlign': 'center'}),
    html.P('''
        This interactive dashboard allows users to explore the GDP per capita across various countries and years, 
        using data from the Gapminder Foundation. Select multiple countries and a range of years to see how 
        GDP per capita has changed over time. The graph below will display the GDP per capita trends for each 
        selected country, illustrating economic growth and development patterns.
    ''', style={'textAlign': 'center'}),


html.Div([
    html.Div([  # Container for the dropdown
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value=['USA'],  # Default selection
            multi=True
        )
    ], style={'width': '10%', 'display': 'inline-block', 'minWidth': '200px'}),  

    html.Div([  # Container for the slider
        dcc.RangeSlider(
            id='year-slider',
            min=int(years[0]),  # min = the first year in the dataset
            max=int(years[-1]),  # max = the last year in the dataset
            value=[1975, 2025],  # Default selected range
            marks={str(year): str(year) for year in range(int(years[0]), int(years[-1])+1, 25)},
            step=1  # Slider moves in increments of 1 year
        )
    ], style={'width': '88%', 'display': 'inline-block', 'verticalAlign': 'top'}),
], style={'display': 'flex', 'justifyContent': 'space-between'}) 

])

# add Graph component in the layout
app.layout.children.append(
    html.Div([
        dcc.Graph(
            id='gdp-graph',  
            figure={
                'data': [],
                'layout': go.Layout(
                    title='GDP Per Capita Over Time',
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'GDP Per Capita (USD)'},
                    hovermode='closest'
                )
            }
        )
    ])
)

# convert GDP per capita values from strings to floats
def gdp_to_float(gdp_str):
    if isinstance(gdp_str, str):
        if 'k' in gdp_str:
            return float(gdp_str.replace('k', '')) * 1000
        else:
            return float(gdp_str)
    return gdp_str

@app.callback(
    Output('gdp-graph', 'figure'),
    [Input('country-dropdown', 'value'), Input('year-slider', 'value')]
)

def update_graph(selected_countries, selected_years):
    traces = []
    for country in selected_countries:
        country_df = df[df['country'] == country]
        # filter for the selected years and convert all GDP values to float
        years = list(range(selected_years[0], selected_years[1] + 1))
        gdp_values = []
        for year in years:
            year_str = str(year)
            if year_str in country_df.columns:
                gdp_values.append(gdp_to_float(country_df.iloc[0][year_str]))
            else:
                gdp_values.append(None) 

        traces.append(go.Scatter(
            x=years,
            y=gdp_values,
            mode='lines+markers',
            name=country
        ))

    # layout for the updated figure
    layout = go.Layout(
        title={
            'text': 'GDP Per Capita Over Selected Years',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis={'title': 'Year'},
        yaxis={
            'title': 'GDP Per Capita (USD)',
            'title_standoff': 25,
            'showgrid': False,
            'tickmode': 'auto',
            'tickformat': ',.0f',
            'automargin': True,
        },
        margin={'l': 40, 'b': 40, 't': 80, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

    return {'data': traces, 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True)