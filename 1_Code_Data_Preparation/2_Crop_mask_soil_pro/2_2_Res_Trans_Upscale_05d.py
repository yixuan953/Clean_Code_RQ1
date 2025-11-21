# This code is used to upscale C and N content from 5km to 0.5 degree and calculate the C:N ratio

import os
import glob
import numpy as np
import xarray as xr
import rasterio
from rasterio.enums import Resampling


# import xesmf as xe

input_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil'
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_N_Cycling' # For the final C:N ratio .nc files

# Step 2: Define the new 0.05-degree grid
new_lons = np.arange(-180, 180, 0.05)
new_lats = np.arange(90, -90, -0.05)

vars = ["SOC", "N"]

for var in vars:
    f1 = os.path.join(process_dir, f"{var}_amount_0-5cm_5km.nc")
    ly1 = xr.open_dataset(f1)

    f2 = os.path.join(process_dir, f"{var}_amount_5-15cm_5km.nc")
    ly2 = xr.open_dataset(f2)

    f3 = os.path.join(process_dir, f"{var}_amount_15-30cm_5km.nc")
    ly3 = xr.open_dataset(f3)

    lat_orig = ly1.lat.values
    lon_orig = ly1.lon.values

    if var == "SOC":
       var_name = "SOC"
    
    if var == "N":
       var_name = "Soil N"
    
    data_ly1 = ly1[var_name][:]
    data_ly2 = ly2[var_name][:]
    data_ly3 = ly3[var_name][:]

    # Calculated SOC and Soil N amount at 5km scale
    sum_all_ly = data_ly1 + data_ly2 + data_ly3
    # Resample the data to 0.05 degree
    resampled_data = sum_all_ly.interp(lat=new_lats, lon=new_lons, method='nearest')

    # Sum up at the 0.5 degree
    avg_data = resampled_data.coarsen(lat=10, lon=10, boundary='trim').sum()

    # Create latitude and longitude arrays
    lat = np.linspace(90 - 0.25, -90 + 0.25, 360, dtype=np.float64)
    lon = np.linspace(-180 + 0.25, 180 - 0.25, 720, dtype=np.float64)
    avg_data = avg_data.assign_coords(lat=("lat", lat), lon=("lon", lon))
    
    output_file = os.path.join(process_dir, f"{var}_top30cm_05d.nc")
    avg_data.to_netcdf(output_file)