import xarray as xr



"""
This function below is a *callback function* used when building the Plotly Dash interface, it will updates plots according to user's input over widgets
variable: string obj
time_index: int obj
"""
def update_graph(variable, time_index):
    selected_var = ds[variable]
    # Plotly graphs
    fig = go.Figure(data=[
    go.Heatmap(z = selected_var.isel(time = time_index),  x=ds['east_west'].values, y=ds['north_south'].values)])
    # Add titles and labels
    fig.update_layout(
        title=f'{variable}',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height = 800,
        width = 1000)
    return fig


"""
This function below will format the datetime values in the following way:
2024-06-02T00:00:00.000000000 to 2024-06-02
datetime_value: 
"""
def format_date(datetime_value):
    return str(datetime_value)[:10]  


"""
This function below takes will slice tthe 
variable: string obj
profile_num: int obj
queried_ds: xarray.Dataset
"""
def profile_selection(variable, profile_num):
    if variable in ['SoilMoist_inst', 'SoilTemp_inst']:
        selected_variable = ds[variable]
        if 'SoilMoist_profiles' in selected_variable.dims:
            queried_ds = selected_variable.isel(SoilMoist_profiles = profile_num)
        if 'SoilTemp_profiles' in selected_variable.dims:
            queried_ds = selected_variable.isel(SoilTemp_profiles = profile_num)
            return queried_ds
    else:
        return

"""

"""
def ZonalStatsToDataFrame(pfaf_id, shapefile, dataset, variable):
    aoi = shapefile[shapefile.PFAF_ID == pfaf_id]
    aoi_mask = regionmask.mask_3D_geopandas(aoi, dataset.east_west, dataset.north_south)
    aoi_ds = dataset[variable].where(aoi_mask)
    summary = aoi_ds.groupby('time').mean(["north_south", "east_west"])
    summary.to_dataframe().reset_index()
    return aoi_df_summary

"""
pfaf_id: int obj
"""
def update_box_plot(pfaf_id):

    return

"""
"""
def build_map():
    
    return