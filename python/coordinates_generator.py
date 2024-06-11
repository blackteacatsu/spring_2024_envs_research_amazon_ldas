import netCDF4 as nc
import numpy as np

# Open the NetCDF file in "append" mode
with nc.Dataset("/Users/kris/amazonforcast/data/202301/LIS_HIST_2023_Jan.nc", 'a') as nc_file:
    # Define coordinates for the dimensions without coordinates
    north_south_coords = np.linspace(6, -21, num=540)  # Example coordinates for "north_south" dimension
    east_west_coords = np.linspace(-82, -49, num=660)  # Example coordinates for "east_west" dimension

    # Create variables for the coordinates
    north_south_var = nc_file.createVariable('north_south', 'f8', ('north_south',), fill_value=np.nan)
    east_west_var = nc_file.createVariable('east_west', 'f8', ('east_west',), fill_value=np.nan)
    #time = nc_file.variables['time']

    # Assign coordinates to the variables
    north_south_var[:] = north_south_coords
    east_west_var[:] = east_west_coords

    # Set attributes for the coordinate variables (if necessary)
    north_south_var.units = 'degrees_n'
    east_west_var.units = 'degrees_e'
    #time.units = "days since 2023-01-01"

    # Attach the coordinate variables to the dimensions
    nc_file.variables['north_south'] = north_south_var
    nc_file.variables['east_west'] = east_west_var

    # Flush changes to the NetCDF file
    nc_file.sync()

# Print a message indicating successful association of coordinates
print("Coordinates added to dimensions 'north_south' and 'east_west'.")
