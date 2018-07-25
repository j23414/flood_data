# Hydro Project --Waterbear

Reproduce analysis from article 
Sadler, Goodall, Morsy, & Spencer. (2018). Modeling urban coastal flood severity from crowd-sourced flood reports using Poisson regression and Random Forest. Journal of Hydrology, 559, 43-55.

### Run jupyter notebooks

1. prepare_flood_events_table.ipynb
   Input: STORM_data_flooded_streets_2010-2016.csv
   Output: flood_events.csv
   
2. make_dly_obs_table_standalone.ipynb
   Input: hampt_rd_data.sqlite (downloaded from hydroshare by the script)
   Output: not_daily_observations.csv
   
3. by_event_for_model.ipynb
   Input: model_flood_counts_rf_ps_cln.r (called from the script)
   Output: for_model_avgs.csv
   
4. plot_count_model_results.ipynb
   Input: poisson_out_test.csv
           poisson_out_train.csv
           rf_out_test.csv
           rf_out_train.csv

### Good luck from waterbear!
