from dash import Dash, html, dash_table, dcc, callback, Output, Input
import xarray as xr
import plotly.graph_objects as go
import plotly.express as px
import dash_ag_grid as dag
import json
import urllib.request
import geopandas as gpd
import regionmask

# Initialize the app
app = Dash(__name__)

# Load and read the geojson file for Italys regions. 
hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'
hybas_sa_lev05 = gpd.read_file(hydrobasins_lev05_url)

with urllib.request.urlopen(hydrobasins_lev05_url) as url:
        jdata = json.loads(url.read().decode())

# Incorporate data
# Here I am using the averaged ensemble value between June 02 to 05
data_location = r'C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05_mean.nc'
# data_location = '/Users/kris/amazonforcast/data/202301/LIS_HIST_2023_Jan.nc'
dataset = xr.open_dataset(data_location)
longitude = dataset.east_west
latitude = dataset.north_south

time = dataset['time']

# Create a function to format the datetime values
def format_date(datetime_value):
    return str(datetime_value)[:10]  # Keep only the date part


# list of variables in the data set
list_of_variables = ['Rainf_tavg', 'Qair_f_tavg',
                     'Qs_tavg','Evap_tavg',
                     'SoilMoist_inst', 'SoilTemp_inst'] 

app.layout = html.Div([
    html.H1(children='Mapping - Forecast Data'),
    html.Hr(),
    dcc.Slider(min=0, max=len(time) - 1, step=4, value=0, marks={i: format_date(time[i].values) for i in range(len(time))}, id='time_index'),
    html.H2(children='Select your variable below'),
    dcc.RadioItems(options=list_of_variables, value='Rainf_tavg', id='var-selector'),
    html.H2(children='Depth'),
    dcc.Dropdown(id='profile-selector', className='',
        options=[{'label': '0-10cm', 'value': '0'}, {'label': '10-40cm', 'value': '1' }, 
                 {'label': '40-100cm', 'value': '2'}, {'label': '100-200cm', 'value': '3'}],
        value='0',
        #placeholder='0'
    ),
    html.Hr(),
    html.Div(id='selected-pfaf-id', style={'fontSize': 20, 'marginTop': '20px'}),
    dcc.Graph(id='map'), dcc.Graph(id='boxplot'),

])

@callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='time_index', component_property='value'),
    Input(component_id='var-selector', component_property='value'),
    Input(component_id='profile-selector', component_property='value')
)

def update_graph(time_index, variable, profile_index):
    # Print statements for debugging purposes
    ## print(f'selected variable is {variable}')
    ## print(f'Time Index: {time_index}, Profile Index: {profile_index}')
    ## print(f'Dimensions of selected variable{dataset[variable].dims}')

    selected_var = dataset[variable]
    if variable == 'SoilMoist_inst': # if user select soil moisture
         fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index, SoilMoist_profiles = int(profile_index)),  x=longitude, y=latitude)])
    
    elif variable == 'SoilTemp_inst': # if user select soil temperature
       fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index, SoilTemp_profiles = int(profile_index)), x=longitude, y=latitude)])

    else:  # when user select any other variables 
        fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index),  x=longitude, y=latitude)])
    
    
    # Iterate through features and create scatter traces for each polygon and multipolygon
    for feature in jdata['features']:
        # Extract the PFAF_ID for hover labels
        pfaf_id = feature['properties']['PFAF_ID']

        # Handle Polygon type
        if feature['geometry']['type'] == 'Polygon':
            # Collect points
            x, y = zip(*feature['geometry']['coordinates'][0])
            # Add scatter trace with hover text
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line=dict(color='#FFFFFF', width=1.5),
                #fill='toself',
                showlegend=False,
                text=[pfaf_id] * len(x),  # Add PFAF_ID
                hoverinfo='text',  # Show only the PFAF_ID as hover text
                hovertemplate='PFAF_ID: %{text}<extra></extra>'
            ))

        # Handle MultiPolygon type
        elif feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                x, y = zip(*polyg[0])
                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    line=dict(color='#FFFFFF', width=1.5),
                    #fill='toself',
                    showlegend=False,
                    text=[pfaf_id] * len(x),  # Add PFAF_ID
                    hoverinfo='text',
                    hovertemplate='PFAF-ID: %{text}<extra></extra>'
                ))

    # Add titles and labels
    fig.update_layout(  
        title=f'{variable}',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height = 600,
        width = 800,
        margin = {'l': 0, 'r': 0, 't': 0, 'b': 0})


    return fig

@callback(
    Output(component_id='boxplot', component_property='figure'),
    Input(component_id='map', component_property='clickData'),
    Input(component_id='var-selector', component_property='value'),
)

def select_region(click_data, variable):
    #print(click_data)
    if click_data and 'points' in click_data:
        # Extract the PFAF_ID from the 'text' field in click data
        pfaf_id = int(click_data['points'][0]['text'])

    else:
        pfaf_id = 61581
    
    aoi = hybas_sa_lev05[hybas_sa_lev05.PFAF_ID == pfaf_id]
    
    # Create a 3d mask - this contains the true / false values identifying pixels
    # inside vs outside of the mask region
    aoi_mask = regionmask.mask_3D_geopandas(aoi,
                                            longitude,
                                            latitude)
    
    # Apply the mask we just made using the shapefile to the raster layer we made
    aoi_ds = dataset[variable].where(aoi_mask)
    summary = aoi_ds.groupby("time").mean(["north_south", "east_west"])
    aoi_ds_summary = summary.to_dataframe().reset_index()

    boxplot = px.box(aoi_ds_summary, y = variable, x = 'time', color='time')
    boxplot.update_layout(title=f'{variable} of Region (PFAF-ID) {pfaf_id}', height = 600, width = 800)

    
    return boxplot

# Run the app
if __name__ == '__main__':
    app.run(debug=True)