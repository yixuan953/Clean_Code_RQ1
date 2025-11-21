#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=60
#SBATCH --mem=25000

#--------------------Environment, Operations and Job steps-------------

# The calculations is based on the following 3 dataset from SoilGrids:
#     1 - Soil organic carbon (dg/kg) for 3 layers (0-5, 5-15, 15-30 cm) at 5 km 
#     2 - Soil bulk density (cg/cm3) for 3 layers (0-5, 5-15, 15-30 cm) at 5 km
#     3 - Soil nitrogen content (cg/kg) for 3 layers (0-5, 5-15, 15-30 cm) at 5 km
#  The data is upscaled to 0-30 cm at 0.5 degree, by aggregating the total SOC and soil N amount [kg] 
#  = (SOC_content or Soil_N_content * BulkDensity * LayerDepth * 5km * 5km)

# Python scripts
# Step1. Calculate total SOC and soil nitrogen amount at 5 km resoution
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/N_cycling_Parameters/Decomposition/2_1_Cal_CN_amount_5km.py

# Step2. Upscale total SOC and soil nitrogen to 0.5 degree and calculate the CN ratio
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/N_cycling_Parameters/Decomposition/2_2_Res_Trans_Upscale_05d.py

# Step3. Calculate the CN ratio at half degree & rename the variable
module load cdo
module load nco
cdo -div /lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil/N_top30cm_05d.nc /lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil/SOC_top30cm_05d.nc /lustre/nobackup/WUR/ESG/zhou111/Data/Para_N_Cycling/NCratio_05d.nc
ncrename -v Soil\ N,NC_ratio /lustre/nobackup/WUR/ESG/zhou111/Data/Para_N_Cycling/NCratio_05d.nc