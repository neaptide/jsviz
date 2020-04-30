# Last modified: Time-stamp: <2020-04-29 15:57:42 haines>
""" Jet stream utilities (jsutil)

"""

import os
import time
import datetime

import netCDF4

import numpy as np
import metpy
import metpy.calc
from metpy.units import units

from skimage.feature import peak_local_max
import cv2

def scanf_datetime(ts, fmt='%Y-%m-%dT%H:%M:%S'):
    """Convert string representing date and time to datetime object"""
    # default string format follows convention YYYY-MM-DDThh:mm:ss
    
    try:
        t = time.strptime(ts, fmt)
        # the '*' operator unpacks the tuple, producing the argument list.
        dt = datetime.datetime(*t[0:6])
    except ValueError as e:
        # value error if something not valid for datetime
        # e.g. month 1...12, something parsed wrong
        dt = None
        
    return dt

def find_months(year, month=1):
    """Find prev, this, and next month to process

    :Parameters:
        year : int value or str 'yyyy_mm'
        month : int value
    :Returns:
        which_months : list of  datetime objects
             [this_month, next_month]
    Examples
    --------
    >>> find_months(2007, 2)
    >>> find_months('2007_02')
    
    """
    if type(year) == int and type(month) == int :
        dt = datetime.datetime(year, month, day=1)
        this_month = dt
    elif type(year) == str :
        dt = scanf_datetime(year, fmt='%Y_%m')
        this_month = dt
    #
    if dt.month == 1: # if January
        # prev_month = datetime.datetime(dt.year-1, month=12, day=1) # Dec
        next_month = datetime.datetime(dt.year, dt.month+1, day=1) # Feb
    elif dt.month == 12: # if December
        # prev_month = datetime.datetime(dt.year, dt.month-1, day=1) # Nov
        next_month = datetime.datetime(dt.year+1, month=1, day=1)  # Jan
    else:
        # prev_month = datetime.datetime(dt.year, dt.month-1, day=1)
        next_month = datetime.datetime(dt.year, dt.month+1, day=1)
    #
    # return (prev_month, this_month, next_month)
    return [this_month, next_month]

def find_jets(d, dtidx=0, p={}):
    """
    Find lat and z of local max winds for each longitude
    at one date/time (dtidx).

    Parameters
    ---------
    d : dict of ndarrays and computed quantities
      from d = get_data(indir,BB)
    dtidx : int
      index of date and time 
    p : dict of parameters used by peak_local_max()
   
    Returns
    -------
    jsidx : numpy array of integers nx4
       columns as [dtidx, zidx, latidx, lonidx] for each peak found
    """

    # p is empty, set some defaults
    if not bool(p):
        p = { 'num_peaks' : 4,
              'min_distance' : 3,
              'exclude_border' : 0,
              'threshold_abs': 40.,
              #
              'peaks_inside_toggle': 1,
              'peaks_inside_threshold': 30.,
              'peaks_inside_zonal_max': 0}

    lons = list(range(0,d['lon'].size))
    jsidx = []

    for lonidx in lons:
      # vertical section at each lonidx of wind speed -- wspd(lvl,lat)
      wsec = d['wspd'][dtidx,:,:,lonidx].squeeze()

      # find lvl and lat where peak winds speeds exceed 30 m/sec and not on border of domain
      # recall wsec.m is metpy array without units
      yx = peak_local_max(wsec.m,
                          min_distance=p['min_distance'],
                          threshold_abs=p['threshold_abs'],
                          exclude_border=p['exclude_border'],
                          num_peaks=p['num_peaks']
                          )
      # number of peaks is number of rows of yx
      numpeaks, _ = yx.shape

      if p['peaks_inside_toggle']:
          # get wind speeds (wspd and uwnd) at peaks
          # bool to track of which peaks to keep 
          keep = np.full(numpeaks, False)
          wspd = np.full(numpeaks, np.NaN)
          uwnd = np.full(numpeaks, np.NaN)
          # get wind speeds and uwnd for each peak
          for i, peak in enumerate(yx):
              lvlidx, latidx = peak # since wsec(lvl,lat)
              uwnd[i] = d['uwnd'][dtidx,lvlidx,latidx,lonidx].m
              wspd[i] = d['wspd'][dtidx,lvlidx,latidx,lonidx].m

              # Find contours of 30 m/s
              # Apply thresholding to the surface and cast as uint8
              # image = np.uint8((wsec.m > 30.0).astype(int))
              image = np.uint8((wsec.m > p['peaks_inside_threshold']).astype(int))

              # transpose image to match order of yx points, # image.T.shape
              # returns tuple (contours, heirarchy) so unpack return as contours, _
              contours, _ = cv2.findContours(image.T,  cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

          # Keep peaks based on:
          #  1. max peak if two or more within one contour (30 m/s)
          #  2. uwnd > 0 (is positive)
          for n, c in enumerate(contours):
              contour = c.squeeze()
              # bool to track which peaks inside contour
              inside = np.full(numpeaks, False)
              for ip, peak in enumerate(yx):
                  pt = tuple(yx[ip,:])
                  try:
                      inside[ip] = (cv2.pointPolygonTest(contour,pt,False) >= 0)
                  except:
                      continue
              # print('lonidx: %d,  cidx: %d,  yx pt inside: %s' % (lonidx, n, inside))
              # of the peaks inside contour which is max and positive eastward
              if inside.any():
                  for ip, val in enumerate(wspd):
                      if (val==max(wspd[inside])) and (uwnd[ip]>0):
                          keep[ip] = True

      # no limitation -- p['peaks_inside_toggle']==False or 0
      else:
          # bool to track of which peaks to keep
          keep = np.full(numpeaks, True)
          
      # 
      for peak in yx[keep]:
          lvlidx, latidx = peak # since wsec(lvl,lat)
          jsidx.append([dtidx,lvlidx,latidx,lonidx])

    # end for each lon
    return np.array(jsidx)

def get_data(indir, BB):
    """ Read in 4d-var ERA5 data

    Parameter
    ---------
    indir : string
       The input directory path. Data loaded by param and by year.
       All param and year files (param.YYYY.nc) in indir must be
       of the same space and time (time, lvl, lat, lon).
    BB : dictionary 
       Requires 4 keys (lat,lon,lvl,dt)
       Each key has value [min, max]

    Returns
    -------
    d : dict of ndarrays and computed quantities

    """

    # key words are used in filename but values are names with netcdf file
    params = {'hgt' : 'geopotential',
              'uwnd': 'u_component_of_wind',
              'vwnd': 'v_component_of_wind',
              'msl' : 'mean_sea_level_pressure'
              }
    
    sfc_params = ['msl']
    press_params = ['hgt', 'uwnd', 'vwnd']
    dt1 = BB['dt'][0]
    dt2 = BB['dt'][1]

    #
    print('Reading ERA5 data from: %s' % indir)

    for param in list(params.keys()):
        fn = '%s.%04d.nc' % (param, dt1.year) # each file year has one param
        # ifn = os.path.join(indir, fn)
        ifn = '/'.join([indir, fn])
        nc = netCDF4.Dataset(ifn)
        varnames = list(nc.variables.keys())
        print(varnames)
        t = nc.variables['time']
        dt = netCDF4.num2date(t[:], units=t.units, calendar=t.calendar)
        lat = nc.variables['latitude'][:].data
        lon = nc.variables['longitude'][:].data
        
        # nonzero returns a tuple of idx per dimension
        # we're unpacking the tuple for each of these idx-vars
        (dtidx,) = np.logical_and(dt >= BB['dt'][0], dt <= BB['dt'][1]).nonzero()
        (latidx,) = np.logical_and(lat >= BB['lat'][0], lat <= BB['lat'][1]).nonzero()
        (lonidx,) = np.logical_and(lon >= BB['lon'][0], lon <= BB['lon'][1]).nonzero()
       
        if param in press_params:
            level = nc.variables['level'][:].data
            (levidx,) =  np.logical_and(level >= BB['lvl'][0], level <= BB['lvl'][1]).nonzero()
            level_units = nc.variables['level'].units
        # get subset of data from file
        if param=='uwnd':
            uwnd = nc.variables['u'][dtidx, levidx, latidx, lonidx].data * units(nc.variables['u'].units)
        elif param=='vwnd':
            vwnd = nc.variables['v'][dtidx, levidx, latidx, lonidx].data * units(nc.variables['v'].units)
        elif param=='hgt':
            geopot = nc.variables['z'][dtidx, levidx, latidx, lonidx].data * units(nc.variables['z'].units)
        elif param=='msl':
            msl = nc.variables['msl'][dtidx, latidx, lonidx].data * units(nc.variables['msl'].units).to('hPa')
        # close the param datafile
        nc.close()

    # -------------------------------
    # do a calculation using metpy functions -- wspd(dt,level,lat,lon)
    wspd = metpy.calc.wind_speed(uwnd, vwnd)
    # compute geopotential height -- hgt(dt,level,lat,lon)
    hgt = metpy.calc.geopotential_to_height(geopot)
    
    # compute height (1d) based on standard pressure -- ht(level)
    ht_std = metpy.calc.pressure_to_height_std(level * units(level_units))
    # we will be adjusting ht from ht_std by difference in msl from
    # std pressure (1013.25 * units.hPa) at sea level
    p0 = 1013.25 * units.hPa
    # difference in pressure to add for each msl(dt,lat,lon)
    pdiff = msl-p0

    # collection of data for plots
    d = dict()
    # dimensions within BB -- nparrays
    d['dt'] = dt[dtidx]
    d['lat']= lat[latidx]
    d['lon']= lon[lonidx]
    d['level']=level[levidx]
    # data already subset to BB and units attached -- Quantity object (nparray * units)
    d['ht_std'] = ht_std # ht(level)
    d['msl'] = msl       # msl(dt,lat,lon)
    d['hgt'] = hgt       # hgt(dt,level,lat,lon)
    d['uwnd']= uwnd      # uwnd(dt,level,lat,lon)
    d['vwnd']= vwnd      # vwnd(dt,level,lat,lon)
    d['wspd']= wspd      # wspd(dt,level,lat,lon)
    d['pdiff']=pdiff     # pdiff(dt,lat,lon)

    return d

def get_coastlines():
    # --------------------------
    # Global Self-consistent, Hierarchical, High-resolution Shoreline Database (gshhs)
    # http://opendap.deltares.nl/thredds/catalog/opendap/noaa/gshhs/catalog.html
    # --- 5 resolutions ----- netCDF versions available on deltars.nl
    # gshhs_f = finest
    # gshhs_h = high
    # gshhs_i = intermediate
    # gshhs_l = low
    # gshhs_c = coarse
    lineurl  = 'http://opendap.deltares.nl/thredds/dodsC/opendap/noaa/gshhs/gshhs_i.nc';
    
    # Get coatline line data: 1D vectors are small, so we can get all data
    # opendap(url_line) # when netCDF4 was not compiled with OPeNDAP
    linedata = netCDF4.Dataset(lineurl)
    
    lines = dict(
        lon=linedata.variables['lon'][:],
        lat=linedata.variables['lat'][:]
        )
    linedata.close()
    # -----------------------------
    return lines

