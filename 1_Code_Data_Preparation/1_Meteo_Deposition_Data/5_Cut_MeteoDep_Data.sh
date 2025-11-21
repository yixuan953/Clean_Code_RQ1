#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000


# This code is used to cut the meteo and deposition data for 4 basins
CutMeteoDepData(){

    meteo_dir="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/Meteo"
    mask_dir="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/1_Global/Masks"

    areas=("Yangtze" "Indus" "LaPlata" "Rhine")

    for area in "${areas[@]}"; do
        echo "=== Processing $area ==="

        range_file="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/2_StudyArea/${area}/range.nc"
        bbox_file="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/2_StudyArea/${area}/bbox.txt"
        bbox=$(cat "$bbox_file")

        meteo_out="/lustre/nobackup/WUR/ESG/zhou111/2_RQ1_Data/2_StudyArea/${area}/Meteo"
        mkdir -p "$meteo_out"

        # === Process the Meteo Data ===
        for file in "$meteo_dir"/*.nc; do
            inname=$(basename "$file")                     
            base=$(echo "$inname" | sed -E 's/_[0-9]{4}-[0-9]{4}//; s/\.nc$//')
                                                           
            outname="${base}_2005-2019.nc"                 

            echo "  Meteo: $inname -> $outname"

            # 1. Cut the meteo data for the four basins
            cdo -L sellonlatbox,$bbox "$file" tmp.nc

            # 2. Select the time range for the data
            cdo -L ifthen "$range_file" -seldate,2005-01-01,2019-12-31 tmp.nc \
                "${meteo_out}/${outname}"

            rm -f tmp.nc
        done

    done

    echo "All done!"
}
#CutMeteoDepData # Uncomment this line to run the function