
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
data_location = r"C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05_mean.nc"
dataset = xr.open_dataset(data_location)

# %%
# define key elements from the dataset
time = dataset['time']
longitude = dataset['east_west'].values
latitude = dataset['north_south'].values
# SoilTemp_profiles = ds['SoilTemp_profiles']
# SoilMoist_profiles = ds['SoilMoist_profiles']
#SoilMoist_inst = dataset['SoilMoist_inst']

# list of variables in the data set
list_of_variables = ['Rainf_tavg', 'Qair_f_tavg',
                     'Qs_tavg','Evap_tavg',
                     'SoilMoist_inst', 'SoilTemp_inst'] 

# Create a function to format the datetime values
def format_date(datetime_value):
    return str(datetime_value)[:10]  # Keep only the date part

# %%
# App layout
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
    dcc.Graph(id='graph1')
])

# %%
# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='time_index', component_property='value'),
    Input(component_id='var-selector', component_property='value'),
    Input(component_id='profile-selector', component_property='value')
)

def update_graph(time_index, variable, profile_index):
    # Print statements for debugging purposes
    print(f"selected variable is {variable}")
    print(f"Time Index: {time_index}, Profile Index: {profile_index}")
    print(f"Dimensions of selected variable{dataset[variable].dims}")

    # Ensure the selected indices are within bounds
    var_dims = dataset[variable].dims
    var_sizes = dataset[variable].sizes
    print(f"Shape of the selected variable: {var_sizes}")

    if 'SoilMoist_profiles' in var_dims:
        if profile_index >= var_sizes['SoilMoist_profiles']:
            raise IndexError('Profile index out of bounds')
    
    if 'time' in var_dims:
        if time_index>= var_sizes['time']:
            raise IndexError('TIme index out of bounds')

    # when user select soil moisture
    if 'SoilMoist_profiles' in dataset[variable].dims:
        print(f"SoilMoist_profiles is a dimension. Profile index: {profile_index}")
        try:
            selected_var = dataset[variable].isel(SoilMoist_profiles=profile_index)
            selected_data = selected_var.isel(time=time_index)
        
        except KeyError as e:
            print(f"KeyError encountered: {e}")

        fig = go.Figure(data=[go.Heatmap(
            z=selected_data.values,
            x=longitude, y=latitude
        )])
        #return fig


    # if variable == 'SoilMoist_inst':
        #print(variable)
        #selected_var = SoilMoist_inst
        #fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index, SoilMoist_profiles = profile_index),  x=longitude, y=latitude)])
    
    # if user select soil temperature
    # if variable == 'SoilTemp_inst':
        #print(ds[variable])
        #selected_var = ds[variable].isel(SoilTemp_profiles = profile_index)
        #fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index),  x=longitude, y=latitude)])
    
    # when user select any other variables
    else: 
        selected_var = dataset[variable]
        fig = go.Figure(data=[go.Heatmap(z = selected_var.isel(time = time_index),  x=longitude, y=latitude)])
    
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