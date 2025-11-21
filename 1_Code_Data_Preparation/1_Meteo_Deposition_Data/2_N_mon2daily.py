import xarray as xr
import numpy as np
import pandas as pd

# Paths
input_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Deposition/N_deposition_monthly_1980-2020.nc"
output_file_monthly = "/lustre/nobackup/WUR/ESG/zhou111/Data/Deposition/N_dep_total_monthly_small.nc"
output_file_daily = "/lustre/nobackup/WUR/ESG/zhou111/Data/Deposition/N_dep_daily_1980-2020.nc"

# Step 1: Open monthly dataset without decoding times
ds = xr.open_dataset(input_file, decode_times=False)

# Step 2: Keep only N_total_dep and convert to float32
ds = ds[['N_total_dep']].astype('float32')

# Step 3: Create datetime index from months
time_in_months = ds['time'].values
dates = pd.date_range(start='1850-01-01', periods=len(time_in_months), freq='MS')
ds = ds.assign_coords(time=dates)

# Step 4: Now you can safely resample to daily
days_in_month = ds.time.dt.days_in_month
daily_index = pd.date_range(ds.time[0].values, ds.time[-1].values + pd.offsets.MonthEnd(0), freq='D')
ds_daily = ds.resample(time='1D').ffill() / days_in_month.resample(time='1D').ffill()

# -----------------------------
# Save daily NetCDF
# -----------------------------
ds_daily.to_netcdf(
    output_file_daily,
    format="NETCDF4",
    encoding={"N_total_dep": {"zlib": True, "complevel": 4, "dtype": "float32"}}
)
print(f"✅ Saved daily file: {output_file_daily}")
