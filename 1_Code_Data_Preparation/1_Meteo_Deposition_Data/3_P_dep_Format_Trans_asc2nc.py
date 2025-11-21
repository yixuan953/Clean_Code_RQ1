# This code is used to transform the P deposition .asc into .nc file

import rasterio
import numpy as np
import xarray as xr
import os

# Path to your .asc file
raw_data_path = "C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Deposition"
asc_file_name = 'P_deposition_kgP_ha.asc'
asc_file = os.path.join(raw_data_path, asc_file_name)

output_path = "C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Deposition/NP_deposition_annual"
nc_file_name = 'P_depostion_annual.nc'
nc_file = os.path.join(output_path, nc_file_name)


# Read the .asc file using rasterio
with rasterio.open(asc_file) as src:
    P_total_dep = src.read(1)  # Read the first band
    transform = src.transform  # Affine transform for georeferencing
    crs = src.crs  # Coordinate reference system
    ncols, nrows = src.width, src.height  # Dimensions of the raster

# Create an xarray DataArray from the raster data
latitudes = np.linspace(src.bounds.top, src.bounds.bottom, nrows)
longitudes = np.linspace(src.bounds.left, src.bounds.right, ncols)

data_array = xr.DataArray(
    P_total_dep, 
    coords=[('lat', latitudes), ('lon', longitudes)], 
    dims=['lat', 'lon'],
    attrs={'units': 'Kg P ha-1 y-1 '}
)

data_array = data_array.where(data_array != -9999, other=np.nan)
data_array.name = 'P_total_dep'

# Convert to NetCDF and save
data_array.to_netcdf(nc_file)