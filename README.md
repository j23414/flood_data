# Flood Data
*Write project description here*

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
git clone https://github.com/matthewdmanning/flood_data.git -b containers
```

### Pull Hydroshare Data
```
$ cd flood_data/data
$ bash ../code/fetchdata.sh
$ ls

38a4ce62960942b4ad8398ee58a777cf.zip 5db7884111fb4662a13f64707c0c6890.zip 9e1b23607ac240588ba50d6b5b9a49b5.zip
41c8d8f8788c4ba0b0bfbb924fe1d403.zip 6c9e9239f70a421b8c49ae642a7b9291.zip b56fea2856bc468bb0e32fc0ad8f910e.zip
50c26ff32a1f461090a36eb0099dad76.zip 712cd2ce8f604c8f824d6836ee3fcb53.zip fb2775104b554f4da0dc1045192caf6f.zip
54df00b15c02458685fa3b622f2ecc7b.zip 77314eb264c84bb6833cf19e8ade03a9.zip ff8be5aea3224c15b262bfddd5fb6033.zip
```

### Pipeline

<img src="https://github.com/matthewdmanning/flood_data/blob/containers/imgs/sadler_JoH_resource_diagram.png" width="600" alt="Sadler's Pipeline">
