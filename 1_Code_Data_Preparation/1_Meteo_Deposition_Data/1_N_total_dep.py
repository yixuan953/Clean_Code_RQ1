# This code is used to calculate the N deposition (1901 - 2021):
    # 1. Transform the unit from [gN m-2 month-1] to [kg N ha-1 month-1]
    # 2. Put oxidized N deposition (noy: NOx) and the reduced N depositon (nhx: NH3) into the same .nc file
    # 3. Sum up the total N deposition
    # 4. Upscale the monthly N deposition into annual scale (in case annual N deposition is needed)

import xarray as xr
import netCDF4
from netCDF4 import Dataset
import cftime
import os

# Load the .nc file
raw_data_path = "C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Deposition/N_deposition_monthly"
input_file_nhx = "ndep-nhx_histsoc_monthly_1901_2021.nc"
input_file_noy = "ndep-noy_histsoc_monthly_1901_2021.nc"
output_file = "N_depostion_monthly.nc"

raw_nhx = os.path.join(raw_data_path, input_file_nhx)
raw_noy = os.path.join(raw_data_path, input_file_noy)
output_N_dep = os.path.join(raw_data_path, output_file)

# Open the original .nc files and extract the lon and lat
ds1 = xr.open_dataset(raw_nhx, decode_times=False)
ds2 = xr.open_dataset(raw_noy, decode_times=False)
print(ds2.variables)

lat = ds1["lat"]
lon = ds1["lon"]
time = ds1["time"]

# Create a new .nc file
new_ds = xr.Dataset(coords={"lat": lat, "lon": lon, "time": time})
 
# Copy "noy" and "nhx" and transform the unit

new_ds["nhx"] = ds1["nhx"] * 10
print("nhx is read")
print(new_ds["nhx"].shape)
new_ds["nhx"].attrs["units"] = "kg N ha-1 month-1"
ds1.close()

new_ds["noy"] = ds2["noy"] * 10
print("noy is read")
print(new_ds["noy"].shape)
new_ds["noy"].attrs["units"] = "kg N ha-1 month-1"
ds2.close()
   
# Sum up the total N deposition
new_ds["N_total_dep"] = new_ds["nhx"] + new_ds["noy"]
new_ds["N_total_dep"].attrs["units"] = "kg N ha-1 month-1"

# Save to a new file
new_ds.to_netcdf(output_N_dep)

print(f"Transformed file saved to: {output_N_dep}")