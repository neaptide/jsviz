# jsviz

[![DOI](https://zenodo.org/badge/255734585.svg)](https://zenodo.org/badge/latestdoi/255734585)

<!-- mybinder.org fails to load required pip module which breaks the code. Taking the demo offline.
<a href="https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb"><img align="right" src="https://mybinder.org/badge_logo.svg"></a>
--->
### Overview
Jet streams are narrow bands of strong winds in the upper troposphere and have dominant influences over short-term weather patterns, and long-term climate and global temperatures.  The Jet Stream Visualization Tool (jsviz) is a graphical tool to help see the variable path of the strongest wind speeds in the upper atmosphere and how these maximum winds evolve with time and space.  Combined with data layers of geopotential height and surface pressure, the tool helps provide understanding of the basic atmospheric dynamics associated with the jet stream.  The tool is also used for evaluating the algorithm for determining the position of the jet stream and how it varies with time, latitude, longitude and altitude. 
<!-- Comparing position and strength of the jet stream with ocean and atmosphere observations -->

The tool provides a map and vertical section (along a given longitude) to view atmospheric pressure highs and lows and high wind features.  [ECMWF Reanalysis (ERA5)](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5) [1] data of wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl) fields are displayed.  Currently, the extents of the map and data focus on North America and hence the atmospheric jets in the northern hemisphere.  These extents can be adjusted in code and data downloaded from ERA5 for other regions of the world.

### The Graphical Tool

The main map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, black lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed) for North America. The section plot on the right displays the longitudinal slice through the upper atmosphere showing the detailed vertical structure of wspd and equal surfaces of hgt (solid black line for 300 hPa and solid blue for other) with altitude (km). By using the graphical interface, longitudes and times can be selected to show (or "play") the 4-dimensional (4D), dynamic nature of the upper atmosphere and the jet stream paths in northern hemisphere. Furthermore, the positions of the jet stream based on the algorithm (red dots) are also displayed, as they vary across the region with time. 

Here is a screen image of the map and interface. 

![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/images/run_jsviz_ipynb.png)

### [Determining Jet Stream Location](https://github.com/neaptide/jsviz/blob/master/jsalgo.md)

There are many different ways that jet stream locations are determined in the literature using reanalysis data.  The algorithm employed in this version of the `jsviz` tool is as follows: 
- Find maximum wind speeds in upper troposhere, using 4D ERA5 data, for each longitude at a given time.
- Apply further limitations when mulitple peaks are found

More details of the method are provided in the [Jet Stream Characterization page](https://github.com/neaptide/jsviz/blob/master/jsalgo.md). 

<!-- mybinder.org fails to load required pip module which breaks the code. Taking the demo offline.
### Quick Start -- Demo

A Binder image has been built to demo the code. This demo can be run if you don't have python setup locally or don't know how to launch your own jupyter-notebook.  Although, it is slower to load and run than downloading and running `jsviz` code locally. 

Launch a the demo Jupyter Notebook from this badge.  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb)

It will open the notebook in a web browser tab. It takes a short while for the page to be displayed.  Be patient.  If it is taking a really long time, most likely there were underlying code changes and the Binder image is being rebuilt. Once the Binder image is (built and) served it will open up notebook called `run_jsviz.ipynb` in a web browser tab. 
-->

### Get the code 

You can clone the [jsviz Github Repository](https://github.com/neaptide/jsviz) or download the zipped code from Github: 

```bash
git clone https://github.com/neaptide/jsviz.git
```

or download and unzip the code:

```bash
wget https://github.com/neaptide/jsviz/archive/master.zip
```

### Build environment 

Once the code is downloaded locally, you will be using the `environment.yml` file in the code folder to get all the dependencies to build an environment with default name `test_jsviz`.  You can use a different enviroment name by editing the `environment.yml`. 

For this example the code is unzipped or cloned into `C:\your\home\jsviz`
 
Open a terminal that activates Anaconda base environment. 
Change the working directory to where you unpacked the code and create the `test_jsviz` environment  

```
(base) C:\your\home> cd jsviz
(base) C:\your\home\jsviz>conda env create -f environment.yml
```

Activate the `test_jsviz` environment
 
```
(base) C:\your\home\jsviz>conda activate test_jsviz
(test_jsviz) C:\your\home\jsviz>
```
 
You can now run `jsviz.py` in either IPython or in a Jupyter Notebook. 

### Running `jsviz.py` in Ipython

Open an Ipython terminal.
```
(test_jsviz) C:\your\home\jsviz>ipython
```

In Ipython, use the magic command `%run` to run the `jsviz.py` code for the specified year and month (YYYY_MM). 

``` 
[1] %run jsviz.py 2018_01
```

This will initialize the interactive graph, previously described, to the first day and hour of that month on the map and you can begin using the interface. The veritcal section will iniatilize to the the first (left-most) longitude of the area.  For example, if `2018_01` is used, the map and vertical section will show the data for 2018-01-01 at 00:00 (UTC) and the longitude of 140 W.


### Running `jsviz.py` in Jupyter Notebook

Start the Jupyter Notebook for your web browser.
```
(test_jsviz) C:\your\home\jsviz>jupyter-notebook
```

Find and open the `run_jsviz.ipynb` notebook.  

You should see a code cell with the following code. Once the cell is run, it will load data for a specified year and month (YYYY_MM).  

```
%matplotlib notebook
%run jsviz.py 2018_01
```

To run the cell block:
- Place the cursor within cell.
- Change `2018_01` (YYYY_MM) to run a different year and month (1979-2019).
- Press "Run" (![run button](https://github.com/neaptide/jsviz/blob/master/images/run_button.png)) to run the cell.  

Once the "Figure 1" bar with the interaction button (![interaction_button](https://github.com/neaptide/jsviz/blob/master/images/interaction_button.png)) is displayed, you can now use the graphical interface. The graph will be initialized to the first day and hour of that month on the map.  The veritcal section will iniatilize to the the first (left-most) longitude of the area.  For example, if `2018_01` is used, the map and vertical section will show the data for 2018-01-01 at 00:00 (UTC) and the longitude of 140 W.

### Using the interactive display

- Select another longitude by moving the "Long" slider or pressing left- (<) and right-arrow (>) associated with it.  
- Select a different time and date by moving the "Date" slider or pressing left- (<) and right-arrow (>) associated with it.
- See the [Jet Stream Characterization](https://github.com/neaptide/jsviz/blob/master/jsalgo.md) description for "Local Maxima Detection" parameters and further peak limitation.
  - Press "Jet Stream ON/OFF" button to toggle display of jet stream markers.
  - Press "Limitation ON/OFF" button to enable/disable further limitation of jet stream algorithm.


### Dependencies

`jsviz` has dependency on the following Python modules:

  - numpy
  - matplotlib
  - metpy
  - netCDF4
  - scikit-image
  - opencv-python

### Acknowledgements

The `jsviz` tool is based upon work supported by National Science Foundation under grant OCE-1558920. 

### References

[1] Copernicus Climate Change Service (C3S) (2017): ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate . Copernicus Climate Change Service Climate Data Store (CDS), date of access. https://cds.climate.copernicus.eu/cdsapp#!/home
