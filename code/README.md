# Pipeline

**Dependencies**

* R 3.4.4
* Python 2.7
* Python pandas
* Python matplotlib

**Move Required Files to this folder**

* `hampt_rd_data.sqlite`


Run the following:

```
../code/fetchdata.sh
python make_dly_obs_table_standalone.py
python prepare_flood_events_table.py
python by_event_for_model.py
Rscript model_flood_counts_rf_ps_cln.r
python plot_count_model_results.py out
```

## Docker Image

Building image takes a while since it's installing r-base and python.

```
docker build -t waterbear .
```

Running the docker image and scripts requires at least 8GB memory. 

<img src="https://github.com/matthewdmanning/flood_data/blob/containers/docs/dockersettings.png" width="400" alt="Docker Settings">

Either run Docker interactively (using the same commands above) or through the provided `script.sh`.

```
docker run -it -v ${PWD}:/data/ waterbear:latest
docker run -v ${PWD}:/data/ waterbear:latest /data/script.sh
ls -ltr

-rw-r--r--  1 username  staff   1.5K Jul 25 21:24 Dockerfile
-rwxr-xr-x  1 username  staff   505B Jul 25 22:18 script.sh
-rw-r--r--  1 username  staff   139K Jul 25 22:45 out_results_together.png
-rw-r--r--  1 username  staff    87K Jul 25 22:45 results_poisson_out.png
-rw-r--r--  1 username  staff    86K Jul 25 22:45 results_rf_out.png
-rw-r--r--  1 username  staff    45K Jul 25 22:45 out_results_together.eps
-rw-r--r--  1 username  staff    28K Jul 25 22:45 results_poisson_out.eps
-rw-r--r--  1 username  staff    28K Jul 25 22:45 results_rf_out.eps
-rw-r--r--  1 username  staff    82K Jul 25 22:45 event_data.csv
-rw-r--r--  1 username  staff   128K Jul 25 22:45 flood_events.csv
-rw-r--r--  1 username  staff   397K Jul 25 22:45 for_model_avgs.csv
-rw-r--r--  1 username  staff   1.5M Jul 25 22:45 nor_daily_observations_standalone.csv
-rw-r--r--  1 username  staff   672K Jul 25 22:45 poisson_out_test.csv
-rw-r--r--  1 username  staff   1.5M Jul 25 22:45 poisson_out_train.csv
-rw-r--r--  1 username  staff   665K Jul 25 22:45 rf_out_test.csv
-rw-r--r--  1 username  staff   1.5M Jul 25 22:45 rf_out_train.csv
-rw-r--r--  1 username  staff    33K Jul 25 22:45 rf_impo_out
```