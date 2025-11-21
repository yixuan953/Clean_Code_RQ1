#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#--------------------Environment, Operations and Job steps-------------

# Step 1 - Transform the N, P deposition from original dataset to .nc format at half degree
# module load python/3.12.0
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Deposition/1_N_dep.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Deposition/2_P_dep_Format_Trans_asc2nc.py


# Step 2 - Downscale N, P deposition to daily scale
module load cdo
input_dir="/lustre/nobackup/WUR/ESG/zhou111/Data/Deposition"
process_dir="/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Deposition"
output_dir="/lustre/nobackup/WUR/ESG/zhou111/Data/Deposition"

# Downscale N deposition (1901-2021) to daily
get_N_daily_dep() {
    # source /home/WUR/zhou111/miniconda3/etc/profile.d/conda.sh
    # conda activate myenv
    # python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Deposition/1_N_mon2daily.py
    # conda deactivate
    
    # Correct the time dimension 
    # cdo settaxis,1980-01-01,00:00:00,1day /lustre/nobackup/WUR/ESG/zhou111/Data/Deposition/N_dep_daily_1980-2020.nc /lustre/nobackup/WUR/ESG/zhou111/Data/Deposition/N_dep_1980-2020_daily.nc

}

# get_N_daily_dep


# Downscale P deposition (2000) to daily (1980-2020)
get_P_daily_dep() {

    cdo -setreftime,2000-01-01,00:00:00 -settaxis,2000-01-01,00:00:00,1year ${input_dir}/P_deposition_annual_2000.nc ${process_dir}/p_dep_with_time.nc
    cdo -setreftime,1980-01-01,00:00:00 -settaxis,1980-01-01,00:00:00,1day -duplicate,14975 ${process_dir}/p_dep_with_time.nc ${process_dir}/p_dep_daily_grid.nc
    cdo -divc,365 ${process_dir}/p_dep_daily_grid.nc ${process_dir}/p_dep_daily_uniform.nc
    cdo -setattribute,title="P_total_dep",unit="kg P ha-1 d-1",method="Uniform temporal downscaling" ${process_dir}/p_dep_daily_uniform.nc ${output_dir}/P_dep_daily_1980-2020.nc

    echo "P deposition downscaled to daily (1901-2021)"
}
# get_P_daily_dep