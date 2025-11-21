# This code is used to calculate the C:N ratio using the data from SoilGrids: https://files.isric.org/soilgrids/latest

import rasterio
import numpy as np
import glob
import os
import xarray as xr

# Path for required data
input_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Soil/CN_ratio_cal'
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil' 
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_N_Cycling' # For the final C:N ratio .nc files

layers = ["0-5cm", "5-15cm", "15-30cm"]

# Calculate the C and N content for each layer at 5 km resolution 
for ly in layers:
    
    f_bdod = os.path.join(input_dir, f"Reproject_bdod_{ly}_mean_5000.tif") 
    with rasterio.open(f_bdod) as src_bdod:
        bdod = src_bdod.read(1).astype(float) # Unit: cg/cm3
        bdod[bdod <= 0] = np.nan
        lon = np.linspace(src_bdod.bounds.left, src_bdod.bounds.right, src_bdod.width)
        lat = np.linspace(src_bdod.bounds.top, src_bdod.bounds.bottom, src_bdod.height)

    f_SoilN = os.path.join(input_dir, f"Reproject_nitrogen_{ly}_mean_5000.tif")
    with rasterio.open(f_SoilN) as src_SoilN:
        SoilN = src_SoilN.read(1).astype(float) # Unit: cg/kg
        SoilN[SoilN <= 0] = np.nan
    
    f_soc = os.path.join(input_dir, f"Reproject_soc_{ly}_mean_5000.tif")
    with rasterio.open(f_soc) as src_soc:
        soc = src_soc.read(1).astype(float) # Unit: dg/kg
        soc[soc <= 0] = np.nan
    
    # The layer depths for further calculations
    if ly == "0-5cm":
        depth = 5
    if ly == "5-10cm":
        depth = 10 
    if ly == "15-30cm":
        depth = 15

    area = 25 # Unit: km2

    SOC_amount = soc * bdod * depth * area * 10.0 # Unit: kg
    N_amount = SoilN * bdod * depth * area * 1.0 # Unit: kg
    
    data_SOC = np.full((len(lat), len(lon)), np.nan, dtype=np.float32)  # Initialize as NaN-filled array
    data_SOC[:] = SOC_amount  # Assign the SOC amounts to the entire array
    data_SOC[data_SOC <= 0] = np.nan
    ds_SOC = xr.Dataset(
            {"SOC": (["lat", "lon"], data_SOC)},
            coords={"lat": lat, "lon": lon},
            attrs={"units": "kg"} # Replace with the actual units
        )
    output_SOC = os.path.join(process_dir, f"SOC_amount_{ly}_5km.nc")
    ds_SOC.to_netcdf(output_SOC)    

    data_N = np.full((len(lat), len(lon)), np.nan, dtype=np.float32)  # Initialize as NaN-filled array
    data_N[:] = N_amount  # Assign the SOC amounts to the entire array
    data_N[data_N <= 0] = np.nan
    ds_N = xr.Dataset(
            {"Soil N": (["lat", "lon"], data_N)},
            coords={"lat": lat, "lon": lon},
            attrs={"units": "kg"} # Replace with the actual units
        )
    output_N = os.path.join(process_dir, f"N_amount_{ly}_5km.nc")
    ds_N.to_netcdf(output_N) 