Bootstrap: docker
From: ubuntu

%post
    apt-get update
    apt-get install -y python2.7 wget python-pip
    pip install --upgrade pip==9.0.3
    pip install jupyter
    pip install numpy
    pip install matplotlib 
    pip install pandas
    apt-get install -y libopenblas-dev r-base-core libcurl4-openssl-dev libopenmpi-dev openmpi-bin openmpi-common openmpi-doc openssh-client openssh-server libssh-dev wget vim git nano git cmake  gfortran g++ curl wget python autoconf bzip2 libtool libtool-bin python-pip python-dev
    apt-get autoremove -y
    apt-get clean && apt-get update
    apt-get install -y locales
    locale-gen en_US.UTF-8
    R --slave -e 'install.packages("caret", repos="https://cloud.r-project.org/")'
    R --slave -e 'install.packages("randomForest", repos="https://cloud.r-project.org/")'    

%files
    STORM_data_flooded_streets_2010-2016.csv
    by_event_for_model.ipynb
    make_dly_obs_table_standalone.ipynb
    model_flood_counts_rf_ps_cln.r
    plot_count_model_results.ipynb
    prepare_flood_events_table.ipynb

%runscript
    export XDG_RUNTIME_DIR=""
    exec /usr/local/bin/jupyter notebook --ip='*' --port=8888 --no-browser
