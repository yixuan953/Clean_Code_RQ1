#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=60
#SBATCH --mem=250000

Cal_global_critical_losses(){
    source /home/WUR/zhou111/miniconda3/etc/profile.d/conda.sh
    conda activate myenv
    python /lustre/nobackup/WUR/ESG/zhou111/1_RQ1_Code/Code_Critical_NP_losses/1_Global_total_critical_losses.py # Get the total critical N, P runoff (from all sectors) [kg]
    # python /lustre/nobackup/WUR/ESG/zhou111/1_RQ1_Code/Code_Critical_NP_losses/2_Global_agri_critical_losses.py # Get the critical total agricultural N, P runoff [kg]
    # python /lustre/nobackup/WUR/ESG/zhou111/1_RQ1_Code/Code_Critical_NP_losses/3_Global_crop_critical_losses.py # Get the critical total cropland N, P runoff [kg]
    # python /lustre/nobackup/WUR/ESG/zhou111/1_RQ1_Code/Code_Critical_NP_losses/4_Global_major_crop_critical_losses.py # Get the critical N, P losses for major crops in unit of kg and kg/ha
    conda deactivate
}
Cal_global_critical_losses

Cut_Range(){
    module load cdo
    module load nco
    StudyAreas=("Rhine" "Yangtze" "LaPlata" "Indus") #("Rhine" "Yangtze" "LaPlata" "Indus")
    data_dir="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/2_StudyArea"
    output_dir="/lustre/nobackup/WUR/ESG/zhou111/3_RQ1_Model_Outputs/Test_CriticalNP/Method1"
    N_runoff="/lustre/nobackup/WUR/ESG/zhou111/3_RQ1_Model_Outputs/Test_CriticalNP/Method1/Global_cropland_critical_N_runoff_kgPerha.nc"
    P_runoff="/lustre/nobackup/WUR/ESG/zhou111/3_RQ1_Model_Outputs/Test_CriticalNP/Method1/Global_cropland_critical_P_runoff_kgPerha.nc"
    N_total_runoff="/lustre/nobackup/WUR/ESG/zhou111/3_RQ1_Model_Outputs/Test_CriticalNP/Method1/Global_maincrop_critical_total_N_runoff.nc"
    P_total_runoff="/lustre/nobackup/WUR/ESG/zhou111/3_RQ1_Model_Outputs/Test_CriticalNP/Method1/Global_maincrop_critical_total_P_runoff.nc"

    

    for StudyArea in "${StudyAreas[@]}"; do

        crop_grid="${data_dir}/${StudyArea}/range.txt"

        # N runoff
        cdo setgrid,/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/grids.txt $N_runoff tmp.nc
        cdo remapnn,$crop_grid tmp.nc ${output_dir}/${StudyArea}_crit_N_runoff_kgperha_fixed.nc
        rm tmp.nc

        # P runoff
        cdo setgrid,/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/grids.txt $P_runoff tmp.nc
        cdo remapnn,$crop_grid tmp.nc ${output_dir}/${StudyArea}_crit_P_runoff_kgperha.nc
        rm tmp.nc

        # Total N runoff
        cdo setgrid,/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/grids.txt $N_total_runoff tmp.nc
        cdo remapnn,$crop_grid tmp.nc ${output_dir}/${StudyArea}_crit_N_runoff_kg.nc
        rm tmp.nc

        # Total P runoff
        cdo setgrid,/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/grids.txt $P_total_runoff tmp.nc
        cdo remapnn,$crop_grid tmp.nc ${output_dir}/${StudyArea}_crit_P_runoff_kg.nc
        rm tmp.nc

    done

}
# Cut_Range