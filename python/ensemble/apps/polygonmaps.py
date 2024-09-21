from dash import Dash, html, dash_table, dcc, callback, Output, Input
import xarray as xr
import plotly.graph_objects as go
import dash_ag_grid as dag
import json
import urllib.request

# Initialize the app
app = Dash(__name__)

# Load and read the geojson file for Italys regions. 
hydrobasins_lev05_url = "https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson"
with urllib.request.urlopen(hydrobasins_lev05_url) as url:
        jdata = json.loads(url.read().decode())

# Incorporate data
# Here I am using the averaged ensemble value between June 02 to 05
data_location = r"C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05_mean.nc"
dataset = xr.open_dataset(data_location)

time = dataset['time']
# Create a function to format the datetime values
def format_date(datetime_value):
    return str(datetime_value)[:10]  # Keep only the date part

longitude = dataset['east_west'].values
latitude = dataset['north_south'].values

# list of variables in the data set
list_of_variables = ['Rainf_tavg', 'Qair_f_tavg',
                     'Qs_tavg','Evap_tavg',
                     'SoilMoist_inst', 'SoilTemp_inst'] 

# Iterate through features and create scatter traces for each polygon and multipolygon
fig = go.Figure()

fig.add_heatmap()

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
            line=dict(color='#121212', width=1.5),
            fill='toself',
            text=feature['properties']['PFAF_ID'],  # Add PFAF_ID
            hoverinfo='text'  # Show only the PFAF_ID as hover text
        ))
        # Add None to separate polygons if needed

    # Handle MultiPolygon type
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            x, y = zip(*polyg[0])
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line=dict(color='#121212', width=1.5),
                fill='toself',
                text=feature['properties']['PFAF_ID'],  # Add PFAF_ID
                hoverinfo='text',
                hovertemplate=None
            ))

# Update layout settings
fig.update_layout(
    width=1000, 
    height=900,
    showlegend=False, 
    margin={"l": 0, "r": 0, "t": 0, "b": 0}
)


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
    dcc.Graph(figure=fig, id='graph1')
])

@callback(
     Input(component_id="graph1", component_property="clickData")
)
def select_region(click_data):
     print(click_data)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)