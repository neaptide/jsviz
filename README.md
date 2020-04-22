# jsviz

### Overview
The Jet Stream Visualization (jsviz) interactive tool is a map and upper atmospheric section (along a given longitude) and play how these evolve with time.  [ECMWF Reanalysis (ERA5)](https://confluence.ecmwf.int/display/CKB/What+is+ERA5) [1] data of wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl) are displayed. The main map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, black lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed) for North America. The section plot on the right displays the longitudinal slice through the upper atmosphere showing the detailed vertical structure of wspd and equal surfaces of hgt (solid black line for 300 hPa and solid blue for other) with altitude (km). By using the graphical interface, differnt longitudes and times can be viewed to show the whole 4D (lat, lon, z, and time) dynamic and fluid nature of the upper atmosphere and the Jet Stream.

### Jet Stream

The `jsviz` code can be run in a jupyter-notebook or standalone using ipython.

Here is a screen image of the map and interface. 

![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/images/run_jsviz_ipynb.png)

### Quick Start -- Don't know python or Jupyter?
Launch a the Jupyter Notebook to demo this tool from this badge. A Binder image has been built for this purpose. It takes a short while for the to be displayed.  Be patient. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb) 

If it is taking a really long time, most likely there were underlying code changes and the Binder image is being rebuilt. Once the image is (built and) served it will open up notebook called `run_jsviz.ipynb` in a web browser tab.


### Using `run_jsviz.ipynb` Notebook

You should see a code cell.

```
%matplotlib notebook
%run jsviz.py 2018_01
```

A given longitude can be selected by moving the slider or pressing left- (<) and right-arrow (>) labeled "Long".  

### Get code and run in your python environment 

If you are familiar with Python and your system Python installation, you can clone the [jsviz Github Repository](https://github.com/neaptide/jsviz): 

```bash
git clone https://github.com/neaptide/jsviz.git
```

or you can install the latest version using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install git+https://github.com/neaptide/jsviz.git
```
### References

[1] Copernicus Climate Change Service (C3S) (2017): ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate . Copernicus Climate Change Service Climate Data Store (CDS), date of access. https://cds.climate.copernicus.eu/cdsapp#!/home
