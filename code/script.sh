#! /usr/bin/env bash
# Auth: Jennifer Chang, Alice Sun, Matthew Manning, Shuting Yan
# Date: 2018/07/25

cd /flood_data/repro; python make_dly_obs_table_standalone.py
cd /flood_data/repro; python prepare_flood_events_table.py
cd /flood_data/repro; python by_event_for_model.py
cd /flood_data/repro; Rscript model_flood_counts_rf_ps_cln.r
cd /flood_data/repro; python plot_count_model_results.py out

cp /flood_data/repro/*.png /data/.
cp /flood_data/repro/*.eps /data/.
cp /flood_data/repro/*.csv /data/.
cp /flood_data/repro/rf_impo_out /data/.
