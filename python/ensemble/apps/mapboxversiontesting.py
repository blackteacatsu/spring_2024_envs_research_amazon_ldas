from dash import Dash, html, dcc, callback, Output, Input
import xarray as xr
import plotly.graph_objects as go
import json
import urllib.request

# Initialize the app
app = Dash(__name__)

# Load and read the GeoJSON file for Hydrobasins
hydrobasins_lev05_url = "https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson"
with urllib.request.urlopen(hydrobasins_lev05_url) as url:
    jdata = json.loads(url.read().decode())

# Load forecast dataset
data_location = '/Users/kris/amazonforcast/data/202301/LIS_HIST_2023_Jan.nc'
dataset = xr.open_dataset(data_location)
time = dataset['time']

# Format dates for the slider
def format_date(datetime_value):
    return str(datetime_value)[:10]

longitude = dataset['east_west'].values
latitude = dataset['north_south'].values

list_of_variables = ['Rainf_tavg', 'Qair_f_tavg', 'Qs_tavg', 'Evap_tavg', 'SoilMoist_inst', 'SoilTemp_inst']

# App layout
app.layout = html.Div([
    html.H1(children='Mapping - Forecast Data'),
    html.Hr(),
    dcc.Slider(min=0, max=len(time) - 1, step=4, value=0, marks={i: format_date(time[i].values) for i in range(len(time))}, id='time_index'),
    html.H2(children='Select your variable below'),
    dcc.RadioItems(options=list_of_variables, value='Rainf_tavg', id='var-selector'),
    html.H2(children='Depth'),
    dcc.Dropdown(id='profile-selector', options=[{'label': '0-10cm', 'value': '0'}, 
                                                  {'label': '10-40cm', 'value': '1'}, 
                                                  {'label': '40-100cm', 'value': '2'}, 
                                                  {'label': '100-200cm', 'value': '3'}], 
                 value='0'),
    html.Hr(),
    dcc.Graph(id='graph1'),
    html.Div(id='selected-pfaf-id', style={'fontSize': 20, 'marginTop': '20px'})
])

# Callback to update the graph
@callback(
    Output('graph1', 'figure'),
    Input('time_index', 'value'),
    Input('var-selector', 'value'),
    Input('profile-selector', 'value'),
    Input('graph1', 'clickData')
)
def update_graph(time_index, variable, profile_index, click_data):
    selected_var = dataset[variable]
    
    if variable == 'SoilMoist_inst':
        heatmap_data = selected_var.isel(time=time_index, SoilMoist_profiles=int(profile_index))
    elif variable == 'SoilTemp_inst':
        heatmap_data = selected_var.isel(time=time_index, SoilTemp_profiles=int(profile_index))
    else:
        heatmap_data = selected_var.isel(time=time_index)
    
    # Base heatmap of the selected variable
    fig = go.Figure(go.Heatmap(z=heatmap_data, x=longitude, y=latitude))

    # Iterate through features to draw polygons
    for feature in jdata['features']:
        pfaf_id = feature['properties']['PFAF_ID']
        
        # Extract polygon coordinates
        if feature['geometry']['type'] == 'Polygon':
            x, y = zip(*feature['geometry']['coordinates'][0])
            fig.add_trace(go.Scatter(
                x=x, y=y, mode='lines', line=dict(color='#121212', width=1.5),
                fill='toself', showlegend=False,
                text=pfaf_id,  # Use the PFAF_ID for click and hover
                hoverinfo='text',
                hovertemplate='PFAF_ID: %{text}<extra></extra>',
                opacity=0.3  # Slightly transparent to allow seeing the background and keep clickability
            ))

        # Handle MultiPolygon type
        elif feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                x, y = zip(*polyg[0])
                fig.add_trace(go.Scatter(
                    x=x, y=y, mode='lines', line=dict(color='#121212', width=1.5),
                    fill='toself', showlegend=False,
                    text=pfaf_id,  # Use the PFAF_ID for click and hover
                    hoverinfo='text',
                    hovertemplate='PFAF_ID: %{text}<extra></extra>',
                    opacity=0.3  # Slightly transparent to allow seeing the background and keep clickability
                ))

    # If a region was clicked, highlight it
    if click_data and 'points' in click_data:
        selected_pfaf_id = click_data['points'][0]['text']
        
        # Highlight the selected region
        for feature in jdata['features']:
            if feature['properties']['PFAF_ID'] == selected_pfaf_id:
                if feature['geometry']['type'] == 'Polygon':
                    x, y = zip(*feature['geometry']['coordinates'][0])
                    fig.add_trace(go.Scatter(
                        x=x, y=y, mode='lines', line=dict(color='red', width=3),  # Highlight in red
                        fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',  # Semi-transparent red fill
                        showlegend=False,
                        hoverinfo='skip'  # Avoid hover on the highlighted region
                    ))
                elif feature['geometry']['type'] == 'MultiPolygon':
                    for polyg in feature['geometry']['coordinates']:
                        x, y = zip(*polyg[0])
                        fig.add_trace(go.Scatter(
                            x=x, y=y, mode='lines', line=dict(color='red', width=3),  # Highlight in red
                            fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',  # Semi-transparent red fill
                            showlegend=False,
                            hoverinfo='skip'  # Avoid hover on the highlighted region
                        ))

    # Update layout
    fig.update_layout(
        title=f'{variable}',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height=800,
        width=1000,
        margin={"l": 0, "r": 0, "t": 0, "b": 0}
    )

    return fig

# Callback to display the selected PFAF_ID
@callback(
    Output('selected-pfaf-id', 'children'),
    Input('graph1', 'clickData')
)
def select_region(click_data):
    if click_data and 'points' in click_data:
        pfaf_id = click_data['points'][0]['text']
        return f"Selected PFAF_ID: {pfaf_id}"
    return "Click on a region to see its PFAF_ID."

if __name__ == '__main__':
    app.run(debug=True)
