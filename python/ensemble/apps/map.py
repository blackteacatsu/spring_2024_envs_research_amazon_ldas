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
ds = xr.open_dataset(r"C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05_mean.nc")

# %%
ds

# %%
rainf = ds['Rainf_tavg']
time = ds['time']
longitude = ds['lon']
latitude = ds['lat']

# %%
# Plotly graphs

# Add titles and labels
fig.update_layout(
    title='Evapotranspiration',
    xaxis_title='Longitude',
    yaxis_title='Latitude',
    height = 800,
    width = 1000)
#fig.show()


# %%
# App layout
app.layout = html.Div([
    html.Div(children='Mapping - Precipitation Forecast Data'),
    html.Hr(),
    dcc.Slider(0, 3, step=4, value=0, marks={0: '2024-06-02', 1:'2024-06-03', 2:'2024-06-04', 3:'2024-06-05'}, id='time_index'),
    dcc.Graph(figure=fig, id='graph1')
])

# %%
# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='time_index', component_property='value')
)
def update_graph(time_index):
    # dff = df[df.country.isin(['Albania', 'Canada', 'Austria', 'Angola', 'Bahrain', 'Argentina'])]
    # fig = px.histogram(dff, x='continent', y=col_chosen, histfunc='avg', pattern_shape='country', labels={"country": "Countries"})
    fig = go.Figure(data=[
    go.Heatmap(z = rainf.isel(time = 0),  x=ds['east_west'].values, y=ds['north_south'].values),
])

    fig = go.Figure(data=[go.Heatmap(z = rainf.isel(time = time_index),  x=ds['east_west'].values, y=ds['north_south'].values)])
    return fig

# %%
# Run the app
if __name__ == '__main__':
    app.run(debug=True)


