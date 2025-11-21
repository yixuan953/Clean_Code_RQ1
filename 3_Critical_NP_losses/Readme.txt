The critical N, P losses at half degree resolution were calculated based the model outputs from the following two models:
    1 - VIC-WUR: For providing runoff [mm] to calculate the annual critical N, P load [kg] 
        Droppers, B., Franssen, W. H. P., van Vliet, M. T. H., Nijssen, B., and Ludwig, F.: Simulating human impacts on global water resources 
        using VIC-5, Geosci. Model Dev., 13, 5029–5052, https://doi.org/10.5194/gmd-13-5029-2020, 2020.
    2 - IMAGE-GNM: For providing the N, P load from different sectors to distribute the total annual critical N, P losses [kg] to our major crops
        Beusen, A. H. W., Van Beek, L. P. H., Bouwman, A. F., Mogollón, J. M., and Middelburg, J. J.: Coupling global models for hydrology and 
        nutrient loading to simulate nitrogen and phosphorus retention in surface water – description of IMAGE–GNM and analysis of performance, 
        Geosci. Model Dev., 8, 4045–4067, https://doi.org/10.5194/gmd-8-4045-2015, 2015. 
        Data can be freely downloaded from: https://dataportaal.pbl.nl/IMAGE/GNM


========================= Critical N, P losses ==============
Processed data folder: 
    Global data: ../Global/Critical_NP_losses
        - Spatial resolution: Half degree
        - Temporal resolution: Year 2015
        - Dataset content and the original source: 
            1) Global_total_critical_N(P)_load.nc: Total critical N or P load in runoff from all sectors [kg]
            2) Global_agri_critical_N(P)_load.nc: Critical N or P load in runoff from agricultural sector [kg]
            3) Global_cropland_critical_N(P)_load.nc: Total critical N or P load in runoff from all cropland [kg]
            4) Global_maincrop_critical_total_N(P)_runoff.nc: Total critical N or P runoff from major crops [kg] (maize, rice, wheat, soybean)
            5) Global_cropland_critical_N(P)_runoff_kgPerha.nc: Critical N or P runoff from cropland [kg/ha] 
               Here we assume all types of cropland should follow the same critical N, P losses standard

    Four basins: ../BasinName/Critical_NP_losses
        - Spatial resolution: Half degree
        - Temporal resolution: Year 2015
        - Dataset content and the original source: 
            1) BasinName_crit_N(P)_runoff_kg.nc: Total critical N or P runoff from major crops [kg] (maize, rice, wheat, soybean)
            2) BasinName_crit_N(P)_runoff_kgperha.nc: Critical N or P runoff from cropland [kg/ha] 
               Here we assume all types of cropland should follow the same critical N, P losses standard

Code folder: ../Code/3_Critical_NP_losses
    - Content:
        1_Global_total_critical_losses.py: Get total critical N, P load in runoff [kg]
        2_Global_agri_critical_losses.py:: Get critical N or P load in runoff from agricultural sector [kg]
        3_Global_crop_critical_losses.py: Get total critical N or P load in runoff from all cropland [kg] 
        4_Global_major_crop_critical_losses.py: Get critical N or P runoff from major crops in the unit of kg and kg/ha
        5_Cut_Range.sh: Cut the critical N, P runoff [kg] and [kg/ha] for study areas
