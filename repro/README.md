# Pipeline (works on mac)

**Dependencies**

* R 3.4.4
* Python 2.7

**Move Required Files to this folder**

* `hampt_rd_data.sqlite`
* `STORM_data_flooded_streets_2010-2016.csv`


Run the following:

```
python make_dly_obs_table_standalone.py
python prepare_flood_events_table.py
python by_event_for_model.py
Rscript model_flood_counts_rf_ps_cln.r
python plot_count_model_results.py out
```