import netCDF4 as nc

# Specify the path to your NetCDF file
file_path = '/Users/kris/amazonforcast/test/test.nc'

# Open the NetCDF file
with nc.Dataset(file_path, 'r') as nc_file:
    # Now you can access variables, dimensions, and attributes in the NetCDF file
    print(nc_file)
