import netCDF4 as nc
import numpy as np

# Open the NetCDF file in "append" mode
with nc.Dataset('/Users/kris/amazonforcast/test/test.nc', 'a') as nc_file:
    # Define coordinates for the dimensions without coordinates
    north_south_coords = np.linspace(6.5, 18.95, num=250)  # Example coordinates for "north_south" dimension
    east_west_coords = np.linspace(-94.5, -76.55, num=360)  # Example coordinates for "east_west" dimension

    # Create variables for the coordinates
    north_south_var = nc_file.createVariable('north_south', 'f8', ('north_south',), fill_value=np.nan)
    east_west_var = nc_file.createVariable('east_west', 'f8', ('east_west',), fill_value=np.nan)

    # Assign coordinates to the variables
    north_south_var[:] = north_south_coords
    east_west_var[:] = east_west_coords

    # Set attributes for the coordinate variables (if necessary)
    north_south_var.units = 'degrees_n'
    east_west_var.units = 'degrees_e'

    # Attach the coordinate variables to the dimensions
    nc_file.variables['north_south'] = north_south_var
    nc_file.variables['east_west'] = east_west_var

    # Flush changes to the NetCDF file
    nc_file.sync()

# Print a message indicating successful association of coordinates
print("Coordinates added to dimensions 'north_south' and 'east_west'.")
