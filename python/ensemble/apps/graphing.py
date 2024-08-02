import xarray as xr
import geopandas as gpd
from dash import Dash, html, dcc, callback, Input, Output
import regionmask
import plotly.express as px

# Initialize the app
app = Dash(__name__)

# Define shape file location
shp_location = r"C:\Users\Kris\Documents\amazonforcast\gisfiles\hydrobasins shape\hybas_sa_lev05_areaofstudy.shp"
# Define netCDF file location
ds_location = r"C:\Users\Kris\Documents\amazonforcast\data\prakrut\output\LIS_HIST_Forecast_June_02_to_05.nc"

hybas_sa_lev05 = gpd.read_file(shp_location)

with xr.open_dataset(ds_location) as ds:
    hybas_sa_lev05 = hybas_sa_lev05.to_crs(epsg=4326)


# Add controls and build interactions


# Run the app locally
if __name__ == '__main__':
    app.run(debug=True, port=8008)