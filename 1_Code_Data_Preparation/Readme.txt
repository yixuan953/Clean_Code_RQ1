To run the WOFOST-Nutrient model, the following categories of data are required:

1. Meteo and N,P deposition data (meteolist)
2. Crop masks containing soil properties (Masks)
3. Irrigation input (irrilist)
4. Fertilization input (fertlist)

The data source and the processing codes are saved in the following folders:

======================= 1. Meteo and N,P deposition data ======================
Processed data folder: 
    Global data: ../Global/Meteo
    Four basins: ../BasinName/Meteo

    - Spatail resolution: Half degree
    - Temporal resolution: Daily (2005-2019)
    - Data content and source: 
------  Meteodata: obtained from WFDE5 with some minor calculations (few command lines with cdo, so the code is not provided)
        Cucchi M., Weedon G. P., Amici A., Bellouin N., Lange S., Müller Schmied H., Hersbach H., Cagnazzo, C. and Buontempo C. (2022): 
        Near surface meteorological variables from 1979 to 2019 derived from bias-corrected reanalysis, version 2.1. Copernicus Climate 
        Change Service (C3S) Climate Data Store (CDS), DOI: 10.24381/cds.20d54e34 (Accessed on 11-20-2025)
        1) Tmax_daily.nc: Daily maximum temperature [celcius degree] = WFDE5_Tmax - 273.15 (transforming from K to celcius degree)
        2) Tmin_daily.nc: Daily minimum temperature [celcius degree] = WFDE5_Tmin - 273.15 (transforming from K to celcius degree)
        3) SWdown_daily.nc: Daily shortwave radiation [kJ/m2] = WFDE5_SWdown * 86.4 (transforming from W/m2 to KJ m-2 day-1)
        4) Prec_daily.nc: Daily precipitation [mm] = WFDE5_Prec * 86.4 (transforming from kg m-2 s-1 to mm)
        5) Wind_daily.nc: Daily wind speed [m/s] = WFDE5_Wind * 0.747 (transforming the wind speed at 10 m to that at 2 m)
        6) Vap_daily.nc: Daily surface vapor pressure [kPa] = WFDE5_Vap * 0.001 (transforming from pa to Kpa)
------  N deposition: obtained from ISIMIP 3a with some temporal downscaling
        Jia Yang, Hanqin Tian (2023): ISIMIP3a N-deposition input data (v1.3). ISIMIP Repository. https://doi.org/10.48364/ISIMIP.759077.3
        7) N_dep_daily.nc: Daily N deposition [kg N/ha harvested area]
------  P deposition: obtained from Mahowald, N., et al. (2008) with some temporal downscaling
        Mahowald, N., et al. (2008), Global distribution of atmospheric phosphorus sources, concentrations and deposition rates, and 
        anthropogenic impacts, Global Biogeochem. Cycles, 22, GB4026, doi:10.1029/2008GB003240.
        8) P_dep_daily.nc: Daily P deposition [kg P/ha harvested area]

Code folder: ../Code/1_Data_Preparation/1_Meteo_Deposition_Data
    - Content: 
        1_N_dep_total.py: Transform the unit of monthly N deposition, and calculate the total N depostion by summing up noy and nhx
        2_N_mont2daily.py: Downscale monthly N deposition to daily
        3_P_dep_Formate_Trans_asc2nc.py: Transform P deposition from .asc to .nc format
        4_Downscale_dep.bash: Downscale monthly and annual deposition to daily scale and correct the format
        5_Cut_MeteoDep_Data: Cut global data for the 4 studies basin


======================= 2. Crop masks containing soil properties ======================
Processed data folder:    
    Global data: ../Global/Soil_Properties/Soil_Properties.nc
        - Spatail resolution: Half degree
        - Dataset content and the original source: 
------- Parameters for runoff or emission fraction calculations
        1)  Slope [-]:
            Directly obtained from ISIMIP3 without further calculation:
            Schewe, J. & Schmied, M. H. DDM30 river routing network for ISIMIP3. https://doi.org/10.48364/ISIMIP.865475 (2022).
        2)  Climate zone: 
            Calculated based on the annual mean temperature, precipitation, and evapotranspiration from ERA5 
            Data available at: https://cds.climate.copernicus.eu/datasets/multi-origin-c3s-atlas?tab=download
------- Parameters for soil N, P availability calculations 
        3)  NC_ratio: Soil N:C ratio [-]
            Calculated based on the soil organic carbon content and the soil nitrogen content from SoilGrids:
            Data is available from: https://files.isric.org/soilgrids/latest
        4)  PC_ratio: Soil N:C ratio [-]
            Calculated based on SOC from the HSWD using the method of Tipping et al. (2016)
            Tipping, E., Somerville, C.J. & Luster, J. The C:N:P:S stoichiometry of soil organic matter. 
            Biogeochemistry 130, 117–131 (2016). https://doi.org/10.1007/s10533-016-0247-z
        5)  Al_Fe_ox: Oxalate extractable Al and Fe content [mmol/kg soil mass]
        6)  P_Olsen: P Olsen [mmol/kg]
------- Soil properties from HWSD --------
            The variables below were directly obtained from ISIMIP dataset without further calculation:
            Jan Volkholz, Christoph Müller (2020): ISIMIP3 soil input data (v1.0). ISIMIP Repository. https://doi.org/10.48364/ISIMIP.942125
        7)  bulk_density: Soil bulk density [kg/dm]
        8)  clay: Topsoil clay fraction [-]
        9)  texture_class: USDA soil texture class dominant for cropland
     
    Four basins: ../BasinName/Mask  

Data source:


Code folder:../Code/1_Data_Preparation/2_Crop_mask_soil_pro
    - Content: Key parameter calculation processes
        1_Climate_Zone.py: Get the climate zone for the first year fertilizer N2O emisson rate calculation
        2_Cal_CN_ratio.sh: Aggregated soil organic carbon, soil nitrogen to top 30 cm, and upscale to 0.5 degree. Then calculate the NC ratio
        3_Cal_PC_ratio.py: Calculate the PC ratio based on HWSD data SOC using the method from Tipping et al. (2016)
        4_Cal_Al_Fe_ox.sh: Calculate the oxalate extractable Al and Fe content [mmol/kg soil mass]
        5_Cal_P_Olsen.py: Upscale the P Olsen data from 1km to half degree and transform the unit from mg/kg to mmol/kg
        6_Get_crop_para.py: Extract the sowing date, TSUM1 and TSUM2 from potential yield simulations for 4 study areas
        7_Cut_mask_combine.sh: Cut the global soil properties for 4 study areas, and combine them with the sowing date and TSUMs.
