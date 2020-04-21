# jsviz
The Jet Stream Visualization (jsviz) tool reads in ERA5 data to build a graphical interface to view a map and upper atmospheric sections (along a given longitude) and then see how these evolve with time.  The map and section show wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl). The map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, dark lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed).  The `jsviz` code can be run in a jupyter-notebook or standalone using ipython.

Here is a screen image of the map and interface. 

[![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/run_jsviz_ipynb.png)](https://mybinder.org/v2/gh/neaptide/jsviz/master)

## Quick Start -- Don't know python or Jupyter?
Launch the Jupyter Notebook from this badge.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb) 

A Binder image has been built for this purpose. It takes a short while for the  to be displayed.  Be patient. If it is taking a really long time, the Binder image is being rebuilt if underlying code changes or dependencies were made since the last build. Once the image is served it will open up a Jupyter dashboard in a web browser tab.

![Image of online notebook server]()

## `jsviz` Jupyter-Notebook

Click on the link `run_jsviz.ipynb` to open the interactive notebook.  

You should see a code cell.

```
%matplotlib notebook
%run jsviz.py 2018_01
```

## Get code and run in your python environment 

If you are familiar with Python and your system Python installation, you can clone the [jsviz Github Repository](https://github.com/neaptide/jsviz) or you can install the latest version using [pip](http://pypi.python.org/pypi/pip):

```bash
   git clone https://github.com/neaptide/jsviz.git
```

```bash
   pip install git+https://github.com/neaptide/jsviz.git
```

[![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/run_jsviz_ipynb.png)](https://mybinder.org/v2/gh/neaptide/jsviz/master)
