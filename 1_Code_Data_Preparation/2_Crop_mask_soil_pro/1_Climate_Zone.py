# This code is used to assign different climate zone for EF_N2O calculation
# 1 - Cool Moist
# 2 - Cool Dry
# 3 - War Moist
# 4 - Warm Dry

import xarray as xr
import numpy as np
import glob
import os

input_file_t = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Climate/ERA5/t_mean_1985_2015_05deg.nc'
input_file_wb = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Climate/ERA5/wb_mean_1985_2015_05deg.nc'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_N_Cycling'

ds_t = xr.open_dataset(input_file_t)
time = ds_t["time"].values
lat = ds_t["lat"].values
lon = ds_t["lon"].values
t = ds_t["t"].isel(time=0)  # Unit: degreeC
t = t.where((t > -100) & (t < 100))

ds_wb = xr.open_dataset(input_file_wb)
time = ds_wb["time"].values
lat = ds_wb["lat"].values
lon = ds_wb["lon"].values
wb = ds_wb["evspsbl"].isel(time=0)  # Unit: mm

# Assign different climate zone number to deifferent pixels
Climate_Zone = xr.full_like(t, fill_value=np.nan)  # Create an empty array with the same shape

Climate_Zone = xr.where((t <= 10) & (wb < 0), 1, Climate_Zone) # Cool moist
Climate_Zone = xr.where((t <= 10) & (wb >= 0), 2, Climate_Zone) # Cool dry
Climate_Zone = xr.where((t > 10) & (wb < 0), 3, Climate_Zone) # Warm moist
Climate_Zone = xr.where((t > 10) & (wb >= 0), 4, Climate_Zone) # Warm dry

a = xr.DataArray(
    Climate_Zone.data,
    dims=("lat", "lon"),
    coords={
    "lon": lon,
    "lat": lat,
    },
    name = "Climate_Zone",
    attrs={
           "units": "-",
           "description": "# 1-Cool Moist; 2-Cool Dry; 3-Warm Moist; 4-Warm Dry"
            }
)

output_nc_file = os.path.join(output_dir, f"Climate_Zone.nc")    
a.to_netcdf(output_nc_file)
print(f"Climate_Zone has been calculated and saved to {output_nc_file}")