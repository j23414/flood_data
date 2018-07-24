#! /usr/bin/env bash
# Auth: Alice Sun, Jennifer Chang, Matthew Manning
# Date: 2018/07/23

set -e
set -u

current=`pwd`

# Array of file names in Hydroshare.
hampthash="9e1b23607ac240588ba50d6b5b9a49b5"
stormhash="77314eb264c84bb6833cf19e8ade03a9"

#hydrodata=(  54df00b15c02458685fa3b622f2ecc7b ff8be5aea3224c15b262bfddd5fb6033 712cd2ce8f604c8f824d6836ee3fcb53  38a4ce62960942b4ad8398ee58a777cf fb2775104b554f4da0dc1045192caf6f 5db7884111fb4662a13f64707c0c6890 6c9e9239f70a421b8c49ae642a7b9291 41c8d8f8788c4ba0b0bfbb924fe1d403 50c26ff32a1f461090a36eb0099dad7 b56fea2856bc468bb0e32fc0ad8f910e)
hydrodata=( hampthash stormhash )
# Pull from Hydroshare, only if data is not on disk.
for hash in hydrodata; do
	if [[ ! -d ${hash} ]]; then
		if [[ ! -f ${has}.zip ]]; then
			wget https://www.hydroshare.org/django_irods/download/bags/"$hash".zip
		fi
		unzip "$hash".zip
	fi
done

# Set environment variables to reference unzipped data without disturbing metadata. File paths are absolute.
export HAMPT_DATA="${current}/${sqlhash}/data/contents/hampt_rd_data.sqlite"
export STORM_DATA="${current}${stormhash}/data/contents/STORM_data_flooded_streets_2010-2016.csv"

# Check that necessary files exist. If not, quit the script.
if [[ ! -f ${HAMPT_DATA} ]]; then
	printf "File not found: %s\n Ending run.\n" "$HAMPT_DATA"
	return 0
elif [[ ! -f ${STORM_DATA} ]]; then
	printf "File not found: %s\n Ending run.\n" "$STORM_DATA"
	return 0
fi

# Run analysis scripts.
python make_dly_obs_table_standalone.py
python prepare_flood_events_table.py
python by_event_for_model.py
Rscript model_flood_counts_rf_ps_cln.r
python plot_count_model_results.py out
