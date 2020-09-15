#!/usr/bin/env python
# coding: utf-8
# Last modified: Time-stamp: <2020-05-19 16:17:33 haines>
r""" Jetstream catalogue (jscat) tool using ECMWF Reanalysis v5 (ERA5) data

Determines jetstream(s) latitude and level for each time and each
longitude, within bounding parameters, based on find_get() algorithm.
Catalogues position and characteristics (e.g. windspeeds,
geopotential height, and geometric altitude) of each position.

Output:
Write jetstream data to text file in specified directory or
default is current directory

Usage:
Using IPython console, use magic to run code as if at unix prompt

Run all the years and months (see do_all()) 
%run jscat.py
or specify year and month 
%run jscat.py [yyyy_mm] [outdir]

Start ipython in era5 python environment
(era5) C:\Users\haines>ipython

Write data to local directory
In[]: cd Dropbox/peach/era5
In[]: %run jscat.py 2018_01

Write data to another directory 
In[]: cd Dropbox/peach/era5
In[]: %run jscat.py 2018_01 ./data

"""
#
import time
import sys
from jsutil import *

def do_jscat(yyyy_mm, outdir):
    dapdir = 'http://whewell.marine.unc.edu/dods/era5' # 0/80 N
    # Define default data bounds for analysis
    BB = dict( lon=[-140, -50],
               lat=[   0,  80],
               lvl=[ 100, 500],
               dt = [datetime.datetime(2017,1,1), datetime.datetime(2017,2,1)]
               )
    BB['dt'] = find_months(yyyy_mm)

    print(f"Getting data for {yyyy_mm} ... ")
    # tic = time.perf_counter()
    d = get_data(dapdir, BB)
    # toc = time.perf_counter()
    # print(f" ... Time: {toc - tic:0.4f} seconds")

    # setup params for find_jets() algo
    lm = { 'num_peaks' : 4,
           'min_distance' : 3,
           'exclude_border' : 0,
           'threshold_abs': 40.,
           #
           'peaks_inside_toggle': 1,
           'peaks_inside_threshold': 30.,
           'peaks_inside_zonal_max': 0}

    # for a given time find jet stream(s) 3D indices 
    # dtidx = 0
    # jsidx = find_jets(d,dtidx,lm)

    jsidx = np.empty((0,4), dtype=int)
    print(f"Finding jets ... ")
    # tic = time.perf_counter()
    for dtidx, dt in enumerate(d['dt']):
        jsi = find_jets(d,dtidx,lm)
        jsidx = np.vstack((jsidx,jsi))
    # toc = time.perf_counter()
    # print(f" ... Time: {toc - tic:0.4f} seconds")

    # get location data values from indices
    # this helps cleanup notation
    idxdt, idxlvl, idxlat, idxlon = jsidx[:,0],jsidx[:,1],jsidx[:,2],jsidx[:,3]

    # initialize js1 array to hold data (minus JSDT)
    types_str='JSLVL JSLAT JSLON JSHT WSPD UWND VWND HGT'
    c = generate_columns(types_str)
    
    nrows, _ = jsidx.shape
    ncols = len(c)
    js1 = np.ones(shape=(nrows,ncols))*np.nan
    dt = np.zeros(shape=(nrows,1), dtype='U25') 
    
    # get datetimes but convert to string YYYYMMDD_HHMM first for writing to file
    for i, idx in enumerate(idxdt):
        # js[i,c['JSDT']] 
        dt[i] = d['dt'][idx].strftime("  %Y %m %d %H %M %S")

    # get position data
    js1[:,c['JSLAT']] = d['lat'][idxlat]
    js1[:,c['JSLON']] = d['lon'][idxlon]
    js1[:,c['JSLVL']] = d['level'][idxlvl]
    
    # get parameter data from indices metpy (dot.m)
    js1[:,c['WSPD']] = d['wspd'][idxdt, idxlvl, idxlat, idxlon]
    js1[:,c['UWND']] = d['uwnd'][idxdt, idxlvl, idxlat, idxlon]
    js1[:,c['VWND']] = d['vwnd'][idxdt, idxlvl, idxlat, idxlon]
    js1[:,c['HGT']] = d['hgt'][idxdt, idxlvl, idxlat, idxlon]
    
    # compute geometric altitude (height) from pressure level 
    # adjusted for msl pressure at time, lat, lon
    pdiff= d['pdiff'][idxdt, idxlat, idxlon] # pdiff is msl(dt,lat,lon)-1013.25 hPa 
    hts = metpy.calc.add_pressure_to_height(d['ht_std'][idxlvl], pdiff)
    js1[:,c['JSHT']] = hts.m
    
    # pre-pend column of dates to rest of js data
    # this will cause the js1 data to be printed as strings 
    # but that is okay at this step because we are ready to write
    # this out to a text file.
    js = np.column_stack((dt, js1))
    types_str = 'YYYY MM DD hh mm ss ' + types_str

    # want to add a header for file
    desc_str = 'Date       Time     Level Latitude Longitude Altitude Windspeed UWind VWind GeopHeight'
    unit_str = 'YYYY MM DD hh mm ss hPa   deg      deg       km       m/sec     m/sec m/sec m'
    line_str = ('='*len(desc_str))
    
    header_str = f"""# FileDescription: 'Jet Stream Positions'
# YYYY_MM: {yyyy_mm}
# LatExtents: {BB['lat'][0]} to {BB['lat'][1]} (deg)
# LonExtents: {BB['lon'][0]} to {BB['lon'][1]} (deg)
# LvlExtents: {BB['lvl'][0]} to {BB['lvl'][1]} (hPa)
# DateExtents: {BB['dt'][0]} to {BB['dt'][1]} 
# TableColumnTypes: {types_str}
# TableStart:
# {desc_str}
# {unit_str}
# {line_str}
"""
    
    # write out the data
    fn = f"js_{yyyy_mm}.txt"
    ofn = '/'.join([outdir, fn])
    print(f"Writing jets to {ofn} ... ")
    write_jet_data(ofn, header_str, js)
    # this function is using numpy's savetxt 
    # if this gets too unwieldly as text, we can try writing netcdf files 
    # (since we already have netCDF4 imported) or
    # output as matlab data with more investigation
    print(f"Done.")

def run_all(outdir):
    """ runs do_jscat(yyyy_mm, outdir) for """
    # for now do 2017-2018]
    seq = list(range(2017,2019)) # [2017, 2018]
    years = ['%d' % s for s in seq]

    seq = list(range(1,13)) # [1,2,3,...,12]
    months = ['%02d' % s for s in seq] 

    tic = time.perf_counter()
    for year in years:
        for month in months:
            yyyy_mm = f'{year}_{month}'
            print(f"----{yyyy_mm}-----")
            do_jscat(yyyy_mm, outdir)
    
    toc = time.perf_counter()
    print(f"Total Time: {toc - tic:0.4f} seconds")


def main():
    do_all = False
    # set input time string and output directory
    if len(sys.argv)==3:
        yyyy_mm = sys.argv[1]
        outdir = sys.argv[2]
    elif len(sys.argv)==2:
        yyyy_mm = sys.argv[1]
        outdir = '.'
    else:
        do_all = True
        outdir = './data'

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    if do_all:
        run_all(outdir)
    else:
        do_jscat(yyyy_mm, outdir)
    
if __name__ == "__main__":
    main()
