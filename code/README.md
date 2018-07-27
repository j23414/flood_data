# Pipeline

**Dependencies**

* R 3.4.4
* Python 2.7
* Python numpy 1.12.0
* Python matplotlib 2.0.0
* Python pandas 0.22

**Move Required Files to this folder**

* `hampt_rd_data.sqlite`

```
cd code
./fetchdata.sh
```

or 

```
cd code
wget https://www.hydroshare.org/django_irods/download/bags/9e1b23607ac240588ba50d6b5b9a49b5.zip
unzip 9e1b23607ac240588ba50d6b5b9a49b5.zip
mv 9e1b23607ac240588ba50d6b5b9a49b5/data/contents/hampt_rd_data.sqlite .
```

If you want to process the sqlite data then do the following script. However you will need 8Gib of RAM. If you do not then skip to the `by_event_for_model.py` script.

```
python make_dly_obs_table_standalone.py
ls -ltr ../data/
```

The rest of this pipeline should run taking input and putting output files in the `flood_data/data/` folder.

```
python prepare_flood_events_table.py
python by_event_for_model.py
Rscript model_flood_counts_rf_ps_cln.r
python plot_count_model_results.py out
ls -ltr ../data/

total 18400
-rw-r--r--  1   staff   193K Jul 26 10:32 STORM_data_flooded_streets_2010-2016.csv
-rw-r--r--  1   staff   119K Jul 26 11:20 flood_events.csv
-rw-r--r--  1   staff   2.3M Jul 26 11:23 nor_daily_observations_standalone.csv
-rw-r--r--  1   staff   536K Jul 26 11:28 for_model_avgs.csv
-rw-r--r--  1   staff   1.6M Jul 26 11:30 rf_out_train.csv
-rw-r--r--  1   staff   677K Jul 26 11:30 rf_out_test.csv
-rw-r--r--  1   staff   1.5M Jul 26 11:30 poisson_out_train.csv
-rw-r--r--  1   staff   672K Jul 26 11:30 poisson_out_test.csv
-rw-r--r--  1   staff    33K Jul 26 11:30 rf_impo_out
-rw-r--r--  1   staff    87K Jul 26 11:35 results_poisson_out.png
-rw-r--r--  1   staff    29K Jul 26 11:35 results_poisson_out.eps
-rw-r--r--  1   staff    86K Jul 26 11:35 results_rf_out.png
-rw-r--r--  1   staff    29K Jul 26 11:35 results_rf_out.eps
-rw-r--r--  1   staff   138K Jul 26 11:35 out_results_together.png
-rw-r--r--  1   staff    46K Jul 26 11:35 out_results_together.eps
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
