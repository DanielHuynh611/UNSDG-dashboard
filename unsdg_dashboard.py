import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load datasets
world_ghg_total_nona = pd.read_csv('world_ghg_total_nona.csv')
world_ghg_total_nona.set_index('Country Name', inplace=True)

ghg_sector = pd.read_csv('industry_co2.csv')
ghg_sector.replace(0, pd.NA, inplace=True)
ghg_sector.dropna(how='any', inplace=True)
ghg_sector = ghg_sector.rename(columns={
    'IPC1': 'Energy',
    'IPC2': 'Industrial Processes and Product Use',
    'IPCMAG': 'Agriculture',
    'IPC4': 'Waste',
    'IPC5': 'Other'
})

year_list = [str(year) for year in range(1990, 2020 + 1)]

correlations = world_ghg_total_nona[year_list].T.corrwith(pd.Series(range(1990, 2020 + 1), index=year_list))
corr_countries = correlations.sort_values(ascending=False).index

renewable_installation = pd.read_excel('installed_renewable.xlsx')
regions = ['World', 'Oceania', 'Northern Africa', 'Eastern Asia', 'Southern Asia',
           'South-Eastern Asia', 'Central Asia', 'Western Asia', 'Latin America and the Caribbean',
           'Europe and Northern America', 'Sub-Saharan Africa']

region_df = renewable_installation[renewable_installation['GeoAreaName'].isin(regions)]
filtered_df = region_df[(region_df['Type of renewable technology'] == 'ALL')].sort_values(by='Value')

investment_df = pd.read_excel('investment.xlsx')
investment_df = investment_df[(investment_df['Type of renewable technology'] == 'ALL') & 
                              (investment_df['GeoAreaName'].isin(regions))]

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define a set of green shades
green_shades = [
    '#006400',  # DarkGreen
    '#228B22',  # ForestGreen
    '#32CD32',  # LimeGreen
    '#7CFC00',  # LawnGreen
    '#ADFF2F',  # GreenYellow
]

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Greenhouse Gas (GHG) Emissions and Energy Equality Dashboard', style={'text-align': 'center'}),
    html.H3(children="Towards Goal 7 and Goal 13 - United Nations' Sustainable Development Goals", style={'text-align': 'center'}),
    
    # Add the four messages in a 2x2 grid
    html.Div([
        html.Div([
            html.Div("1.5°C", style={'color': 'red', 'font-size': '48px', 'font-weight': 'bold', 'text-align': 'center'}),
            html.Div("will be exceeded by 2035.", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("(United Nations)", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#f0f0f0', 'padding': '20px', 'margin': '1%', 'border-radius': '15px'}),
        
        html.Div([
            html.Div("70%", style={'color': 'red', 'font-size': '48px', 'font-weight': 'bold', 'text-align': 'center'}),
            html.Div("of the annual energy-related CO2 emissions need to decline", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("below today's levels to meet the net-zero climate goal.", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("(United Nations Development Programme)", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#f0f0f0', 'padding': '20px', 'margin': '1%', 'border-radius': '15px'}),
        
        html.Div([
            html.Div("73%", style={'color': 'red', 'font-size': '48px', 'font-weight': 'bold', 'text-align': 'center'}),
            html.Div("of global greenhouse gas emissions originated", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("from the energy sector.", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("(United Nations Development Programme)", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#f0f0f0', 'padding': '20px', 'margin': '1%', 'border-radius': '15px'}),
        
        html.Div([
            html.Div("$4 trillion", style={'color': 'red', 'font-size': '48px', 'font-weight': 'bold', 'text-align': 'center'}),
            html.Div("are needed to reach net-zero by 2050.", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'}),
            html.Div("(United Nations Development Programme)", style={'color': 'black', 'font-size': '22px', 'text-align': 'center'})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#f0f0f0', 'padding': '20px', 'margin': '1%', 'border-radius': '15px'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'}),
    
    dcc.Graph(
        id='ghg-emissions-line-chart',
        figure={
            'data': [
                go.Scatter(
                    x=ghg_sector['year'],
                    y=ghg_sector[col],
                    mode='lines',
                    name=col,
                    line=dict(color='red' if col == 'Energy' else green_shades[i % len(green_shades)]),
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<br>Total GHG: %{y}',
                    text=[col] * len(ghg_sector['year']),  # This will ensure the column name is displayed in the hovertemplate
                    hoverinfo='skip'  # This will hide the default hover information
                ) for i, col in enumerate(ghg_sector.columns[1:])
            ],
            'layout': go.Layout(
                title={'text': 'GHG Emissions Over Time by Sector', 'font': {'size': 24}, 'x': 0.5},
                xaxis_title='Year',
                yaxis_title='CO2 Emissions (Mt)',
                showlegend=True,
                xaxis=dict(showgrid=False),  # Remove x-axis gridlines
                yaxis=dict(showgrid=False),  # Remove y-axis gridlines
                plot_bgcolor='white',  # Set plot background color to white
                paper_bgcolor='white',  # Set paper background color to white
                updatemenus=[
                    {
                        'type': 'buttons',
                        'x': 0.1,
                        'y': 1.15,
                        'buttons': [
                            {
                                'args': ['yaxis.range', [0, 35000]],
                                'label': 'Original',
                                'method': 'relayout'
                            },
                            {
                                'args': ['yaxis.range', [0, 150]],
                                'label': 'Zoom 0-150',
                                'method': 'relayout'
                            },
                        ]
                    }
                ]
            )
        }
    ),
    
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in corr_countries],
            value=corr_countries[0]
        ),
        dcc.Graph(id='country-ghg-line-chart')
    ]),
    
    dcc.Graph(
        id='renewable-tech-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=filtered_df['Value'],
                    y=filtered_df['GeoAreaName'],
                    orientation='h',
                    marker=dict(color='lightgreen')  # Set bar color to light green
                )
            ],
            'layout': go.Layout(
                title={'text': 'Renewable energy-generating capacity by region (2022)', 'font': {'size': 24}, 'x': 0.5},
                xaxis_title='Capacity (watts per capita)',
                xaxis=dict(showgrid=False),  # Remove x-axis gridlines
                yaxis=dict(
                    autorange='reversed',
                    showgrid=False  # Remove y-axis gridlines
                ),
                plot_bgcolor='white',  # Set plot background color to white
                paper_bgcolor='white',  # Set paper background color to white
                margin=dict(l=200)
            )
        }
    ),
    
    html.Div([
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in regions],
            value=regions[0]
        ),
        dcc.Graph(id='renewable-tech-time-series-chart')
    ])
])

# Define callback to update the country GHG line chart
@app.callback(
    Output('country-ghg-line-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_country_ghg_chart(selected_country):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=year_list,
        y=world_ghg_total_nona.loc[selected_country, year_list],
        mode='lines',
        name=selected_country,
        line=dict(color='red' if correlations[selected_country] > 0 else 'lightgreen'),
        hovertemplate='<b>%{text}</b><br>Year: %{x}<br>Total GHG: %{y}',
        text=[selected_country] * len(year_list),  # This will ensure the country name is displayed in the hovertemplate
        hoverinfo='skip'  # This will hide the default hover information
    ))
    fig.update_layout(
        title={'text': f'GHG Emissions Over Time for {selected_country}', 'font': {'size': 24}, 'x': 0.5},
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tick0=1990,
            dtick=3,
            showgrid=False  # Remove x-axis gridlines
        ),
        yaxis=dict(
            title='Total GHG (kt of CO2 equivalent)',
            showgrid=False  # Remove y-axis gridlines
        ),
        plot_bgcolor='white',  # Set plot background color to white
        paper_bgcolor='white'  # Set paper background color to white
    )
    return fig

# Define callback to update the renewable technology time series chart
@app.callback(
    Output('renewable-tech-time-series-chart', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_renewable_tech_time_series(selected_region):
    filtered_region_df = investment_df[investment_df['GeoAreaName'] == selected_region]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_region_df['TimePeriod'],
        y=filtered_region_df['Value'],
        mode='lines+markers',
        name=selected_region,
        line=dict(color='lightgreen'),  # Always set line color to light green
        hovertemplate='<b>%{text}</b><br>Year: %{x}<br>Total GHG: %{y}',
        text=[selected_region] * len(filtered_region_df),  # This will ensure the region name is displayed in the hovertemplate
        hoverinfo='skip'  # This will hide the default hover information
    ))
    fig.update_layout(
        title={'text': f'International financial flows supporting clean <br> energy R&D and renewable energy production {selected_region}', 'font': {'size': 24}, 'x': 0.5},
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tick0=1990,
            dtick=3,
            showgrid=False  # Remove x-axis gridlines
        ),
        yaxis=dict(
            title='Millions of constant USD',
            showgrid=False  # Remove y-axis gridlines
        ),
        plot_bgcolor='white',  # Set plot background color to white
        paper_bgcolor='white'  # Set paper background color to white
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(port=8051, debug=False)