# jsviz
The Jet Stream Visualization (jsviz) tool reads in ERA5 data to build a graphical interface to view a map and upper atmospheric sections (along a given longitude) and then see how these evolve with time.  The map and section show wind speed (wspd), height of the geopotential surface (hgt), and mean sea-level pressure (msl). The map shows the average wspd for the 100-400 hPa levels in filled contours corresponding to the scale below the map, hgt (300 hPa level) in sold, dark lines, and msl in grey lines (>=1013 hPa solid, <1013 hPa dashed).  The `jsviz` code can be run in a jupyter-notebook or standalone using ipython.

Here is a screen image of the map and interface. 

![Image of jsviz window](https://github.com/neaptide/jsviz/blob/master/images/run_jsviz_ipynb.png)

## Quick Start -- Don't know python or Jupyter?
Launch a the Jupyter Notebook to demo this tool from this badge. A Binder image has been built for this purpose. It takes a short while for the to be displayed.  Be patient. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neaptide/jsviz/master?filepath=run_jsviz.ipynb) 

If it is taking a really long time, most likely there were underlying code changes and the Binder image is being rebuilt. Once the image is (built and) served it will open up notebook called `run_jsviz.ipynb` in a web browser tab.


## Using `run_jsviz.ipynb` Notebook

You should see a code cell.

```
%matplotlib notebook
%run jsviz.py 2018_01
```

## Get code and run in your python environment 

If you are familiar with Python and your system Python installation, you can clone the [jsviz Github Repository](https://github.com/neaptide/jsviz): 

```bash
git clone https://github.com/neaptide/jsviz.git
```

or you can install the latest version using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install git+https://github.com/neaptide/jsviz.git
```
