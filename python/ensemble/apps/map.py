# %%
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import xarray as xr
import plotly.graph_objects as go
import dash_ag_grid as dag

# %%
# Initialize the app
app = Dash(__name__)

# %%
# Incorporate data
ds_location = r"C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05_mean.nc"
ds = xr.open_dataset(ds_location)

# %%
ds

# %%

# define key elements from the dataset
time = ds['time']
longitude = ds['lon']
latitude = ds['lat']

# list of variables in the data set
list_of_variables = ['Rainf_tavg','SoilMoist_inst',
                     'Qs_tavg','Evap_tavg','SoilTemp_inst','Qair_f_tavg'] 

# %%
# Plotly graphs
#fig = go.Figure(data=[go.Heatmap(z = rainf.isel(time = 0),  x=ds['east_west'].values, y=ds['north_south'].values)])

# Add titles and labels
# fig.update_layout(title='Rainf_tavg', xaxis_title='Longitude', yaxis_title='Latitude', height = 800, width = 800)
# fig.show()

# %%
# App layout
app.layout = html.Div([
    html.H1(children='Mapping - Forecast Data'),
    html.Hr(),
    dcc.Slider(0, 3, step=4, value=0, marks={0: '2024-06-02', 1:'2024-06-03', 2:'2024-06-04', 3:'2024-06-05'}, id='time_index'),
    html.H2(children='Select your variable below'),
    dcc.RadioItems(options=list_of_variables, value='Rainf_tavg', id='var-selector'),
    html.H2(children='Depth'),
    dcc.Dropdown(id='profile-selector', className='',
        options=[{'label': '0-10cm', 'value': '0'}, {'label': '10-40cm', 'value': '1' }, 
                 {'label': '40-100cm', 'value': '2'}, {'label': '100-200cm', 'value': '3'}],
        value='0',
        placeholder='0'
    ),
    html.Hr(),
    dcc.Graph(id='graph1')
])

# %%
# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='time_index', component_property='value'),
    Input(component_id='var-selector', component_property='value')
)
def update_graph(time_index, variable):
    selected_var = ds[variable]
    # Plotly graphs
    fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index),  x=ds['east_west'].values, y=ds['north_south'].values)])
    # Add titles and labels
    fig.update_layout(
        title=f'{variable}',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height = 800,
        width = 1000)
    return fig



# %%
# Run the app
if __name__ == '__main__':
    app.run(debug=True)




