# Flood Data
Flooding events trigger severe life-threatening issues especially in coastal cities, and therefore, efficient models for flood prediction becomes urgent and essential. However, recent hydrological systems in the coastal areas do not heavily rely on physical data, which enhances the novelty of this project to serve as a data-driven method to predict flooding events. In this project, environmental data including rainfall, water level, wind and tide level, together with the observational data including the flooding reports per storm event were collected in the Norfolk, Virginia USA region from 2010 to 2016. Two data-driven models-Poisson regression and Random Forest regression were trained to predict the flooding severity based on given environmental factors in a storm event. The result shows that Random Forest regression predicts flooding events with lower error rates and false negative rate than that of the Poisson regression. This repository contains all the scripts and datasets that are required to reproduce the figures in the original paper attached here: https://www.sciencedirect.com/science/article/pii/S0022169418300519  

# Environment Setup
To set up conda environment and install Python packages:
> conda env create -f waterbear.yml --name waterbear

> conda activate waterbear

**Dependencies**

* python=2.7
* numpy
* pandas
* sklearn
* sqlite3
* matplotlib
* pydoplus

### Pull github branch

```
git clone https://github.com/matthewdmanning/flood_data.git
cd flood_data
git checkout containers
```

### Pull Hydroshare Data

```
$ cd flood_data/data
$ bash ../code/fetchdata.sh
```

### Pipeline

<img src="https://github.com/matthewdmanning/flood_data/blob/containers/docs/sadler_JoH_resource_diagram.png" width="600" alt="Sadler's Pipeline">

