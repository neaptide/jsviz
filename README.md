# jsviz

The Jet Stream Visualization (jsviz) tool reads in ERA5 data to build a graphical interface to view a map and upper atmospheric sections (along a given longitude) and then see how these evolve with time.  The map and section show wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl). The map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, dark lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed).  Below is an image of the map and interface. 

## Quick Start -- Don't know python
Launch the notebook that runs a server and the code for you. 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master)

## Get code and run in your python environment 

The `jsviz` code can be run in a jupyter-notebook or standalone using ipython. 



A browser tab will open to an interactive jupyter-notebook servered via mybinder.org and will look like the following:

![Image of online notebook server](https://github.com/neaptide/jsviz/blob/master/run_jsviz_notebook_view.png)

The Jupyter Notebook `run_jsviz.ipynb` may need to be rebuilt on mybinder.org by 
Binder may need to be rebuild the interactive notebook, if there have been changes to the underlying code. This can take some time so be patient.

[![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/run_jsviz_ipynb.png)](https://mybinder.org/v2/gh/neaptide/jsviz/master)
