import xarray as xr

# Open the NetCDF file
# ds_1 = xr.open_dataset('/Users/kris/amazonforcast/test/for_arcgis.nc')

ds_2 = xr.open_dataset('/Users/kris/amazonforcast/data/202301/LIS_HIST_2023_Jan.nc')

# Display information about the dataset
# print(ds_1)

print(ds_2)
