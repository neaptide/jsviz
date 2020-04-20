# jsviz
The Jet Stream Visualization (jsviz) tool reads in ERA5 data to build a graphical interface to view a map and upper atmospheric sections (along a given longitude) and then see how these evolve with time.  The map and section show wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl). The map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, dark lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed).  The `jsviz` code can be run in a jupyter-notebook or standalone using ipython.

Here is an image of the map and interface. 

[![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/run_jsviz_ipynb.png)](https://mybinder.org/v2/gh/neaptide/jsviz/master)

## Quick Start -- Don't know python?
Launch an interactive notebook to the code repository from this badge.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master) 

A browser tab will open to an interactive jupyter-notebook servered via mybinder.org.  A Binder image has been built for this purpose. It takes a short while for the  to be displayed.  Be patient. If it is taking a really long time, the Binder image might being rebuilt depending on if there where any underlying code changes or dependencies. Click on `run_jsviz.ipynb` to launch the interactive graph. 

## Get code and run in your python environment 
If you are familiar with Python and your system Python installation, you can install the latest version using [pip](http://pypi.python.org/pypi/pip).

Get the code:
```bash
   pip install git+https://github.com/neaptide/jsviz.git
```

OR download from [Github](https://github.com/neaptide/jsviz)

## Jupyter-Notebook
Once your jupyter-notebook is up and running, you will get screen like the one below. Click on the link `run_jsviz.ipynb`  
![Image of online notebook server](https://github.com/neaptide/jsviz/blob/master/run_jsviz_notebook_view.png)



[![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/run_jsviz_ipynb.png)](https://mybinder.org/v2/gh/neaptide/jsviz/master)
