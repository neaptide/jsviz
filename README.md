# jsviz
<a href="https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb"><img align="right" src="https://mybinder.org/badge_logo.svg"></a>
### Overview
The Jet Stream Visualization Tool (jsviz) is a graphical tool to help see the variable path of the strongest wind speeds in the upper atmosphere and how these maximum winds evolve with time and space.  Combined with data layers of geopotential height and surface pressure, the tool helps provide understanding of the basic atmospheric dynamics associated with the jet stream.  It is also be used for evaluating the algorithm for determining the position of the jet stream and how it varies with time, latitude, longitude and altitude. 

The tool provides a map and vertical section (along a given longitude) to view atmospheric pressure highs and lows and high wind features.  [ECMWF Reanalysis (ERA5)](https://confluence.ecmwf.int/display/CKB/What+is+ERA5) [1] data of wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl) fields are displayed.  Currently, the extents of the map and data focus on North America and hence the atmospheric jets in the northern hemisphere.  These extents can be adjusted in code and data downloaded from ERA5 for other regions of the world.

### The Graphical Tool

The main map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, black lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed) for North America. The section plot on the right displays the longitudinal slice through the upper atmosphere showing the detailed vertical structure of wspd and equal surfaces of hgt (solid black line for 300 hPa and solid blue for other) with altitude (km). By using the graphical interface, longitudes and times can be selected to show (or "play") the 4-dimensional (4D), dynamic nature of the upper atmosphere and the jet stream paths in northern hemisphere. Furthermore, the positions of the jet stream based on the algorithm (red dots) are also displayed, as they vary across the region with time. 

Here is a screen image of the map and interface. 

![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/images/run_jsviz_ipynb.png)

### [Determining Jet Stream Location](https://github.com/neaptide/jsviz/blob/master/jsalgo.md)

There are many different ways that jet stream locations are determined in the literature using reanalysis data.  The algorithm employed in this version of the `jsviz` tool is as follows: 
- Find maximum wind speeds in upper troposhere, using 4D ERA5 data, for each longitude at a given time.
- Apply further limitations when mulitple peaks are found

More details of the method are provided in the [Jet Stream Characterization page](https://github.com/neaptide/jsviz/blob/master/jsalgo.md). 

### Quick Start -- Demo

A Binder image has been built to demo the code. This demo can be run if you don't have python setup locally or don't know how to launch your own jupyter-notebook.  Although, it is slower to load and run than downloading and running `jsviz` code locally. 

Launch a the demo Jupyter Notebook from this badge.  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb)

It will open the notebook in a web browser tab. It takes a short while for the page to be displayed.  Be patient.  If it is taking a really long time, most likely there were underlying code changes and the Binder image is being rebuilt. Once the Binder image is (built and) served it will open up notebook called `run_jsviz.ipynb` in a web browser tab. 

### Using `run_jsviz.ipynb` Notebook

You should see a code cell, and once it is run, will load data for a specified year and month (YYYY_MM).  It will initialize the graph to the first day and hour of that month on the map.  The veritcal section will iniatilize to the the first (left-most) longitude of the area.  For example, if `2018_01` is used, the map and vertical section will show the data for 2018-01-01 at 00:00 (UTC) and the longitude of 140 W.

```
%matplotlib notebook
%run jsviz.py 2018_01
```

To start:
- Place the cursor within cell.
- Change `2018_01` (YYYY_MM) to run a different year and month. (Only 2017-2018 data are currently avialable)
- Press "Run" (![run button](https://github.com/neaptide/jsviz/blob/master/images/run_button.png)) to run the cell.  

Once the "Figure 1" bar with the interaction button (![interaction_button](https://github.com/neaptide/jsviz/blob/master/images/interaction_button.png)) is displayed, you can now use the graphical interface. 
- Select another longitude by moving the "Long" slider or pressing left- (<) and right-arrow (>) associated with it.  
- Select a different time and date by moving the "Date" slider or pressing left- (<) and right-arrow (>) associated with it.
- See the [Jet Stream Characterization](https://github.com/neaptide/jsviz/blob/master/jsalgo.md) description for "Local Maxima Detection" parameters and further peak limitation.
  - Press "Jet Stream ON/OFF" button to toggle display of jet stream markers.
  - Press "Limitation ON/OFF" button to enable/disable further limitation of jet stream algorithm.

### Get the code 

The `jsviz` code can be run in a Jupyter Notebook or standalone using IPython.  If you are familiar with Python and your system Python installation, you can clone the [jsviz Github Repository](https://github.com/neaptide/jsviz): 

```bash
git clone https://github.com/neaptide/jsviz.git
```

or you can install the latest version using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install git+https://github.com/neaptide/jsviz.git
```

### Dependencies

`jsviz` has dependency on the following Python modules:

  - numpy
  - matplotlib
  - metpy
  - netCDF4
  - scikit-image
  - opencv-python


### References

[1] Copernicus Climate Change Service (C3S) (2017): ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate . Copernicus Climate Change Service Climate Data Store (CDS), date of access. https://cds.climate.copernicus.eu/cdsapp#!/home
