# Last modified: Time-stamp: <2020-04-20 10:08:14 haines>
r""" Jetstream vizualization (jsviz) tool using ECMWF Reanalysis v5 (ERA5) data

Plots:

(1) For a given time, show map (hmap) of mean sea level pressure (msl), average of
upper troposphere (100-400 hPa) wind speed (wspd), and geopotential height (hgt).
(2) For a given time and longitude, show vertical section (vsec) of
wspd and hgt through upper troposphere as latitude vs altitude.

GUI:
   Longitude slider with prev and next buttons
   Time slider with prev and next buttons

Usage:
Using IPython console, use magic to run code as if at unix prompt and
provide year and month to view e.g.
%run jsviz.py [yyyy_mm]

Start ipython in era5 python environment
(era5) C:\Users\haines>ipython

In[]: cd Dropbox/peach/era5
In[]: %run jsviz.py 2018_01
In[]: plt.show()

Still TODO:
   (Select how vertical section is plotted: press lvl or standard alt or msl altitude)

"""

import sys
from jsutil import *

import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from matplotlib.widgets import Slider, Button, TextBox, CheckButtons

# Define default bounds and bounding box
BB = dict( lon=[-140, -50],
           lat=[  10,  60],
           lvl=[ 100, 500],
           dt = [datetime.datetime(2017,1,1), datetime.datetime(2017,2,1)]
           )

# grab the coastline dataset
lines = get_coastlines()

# empty array for jet stream indices in data
js = np.array([])
# js column order defined as [JSDT,JSLVL,JSLAT,JSLON]
JSDT=0
JSLVL=1
JSLAT=2
JSLON=3

lm = { 'num_peaks' : 4,
       'min_distance' : 3,
       'exclude_border' : 0,
       'threshold_abs': 40.}


# setup figure layout 
fig = plt.figure(figsize=(10, 7.5))
axs = [fig.add_axes((.1,.1,.6,.7)),0,0]

# main map
title1_str = 'avg wspd (100-400 hPa), hgt (300 hPa), msl pressure (hPa)'
axs[0].set_title(title1_str, loc='left')
t1 = axs[0].set_title('YYYY_MM_DD_HHMM', loc='right')
# set aspect to simply mimic equidistant projection
axs[0].set_aspect(1/np.cos(np.pi*np.mean(BB['lat'])/180.)) 
axs[0].set_xlim(BB['lon'][0],BB['lon'][1])
axs[0].set_ylim(BB['lat'][0],BB['lat'][1])
axs[0].set_xlabel('Longitude (deg)')
axs[0].set_ylabel('Latitude (deg)')
# plot coastline/lakes
axs[0].plot(lines['lon'],lines['lat'],'k',linewidth=0.5)
# plot dotted vertical line at longitude of section plot
l1 = axs[0].axvline(x=0, color='b', linestyle=':', linewidth=3.0)

# wpsd color bar
# get_positions returns Bbox, we want Bbox.bounds
l,b,w,h = axs[0].get_position().bounds
axs[1] = fig.add_axes([l,b-0.075,w,0.02])

# do this now so that we can get adjusted ax get_position
plt.draw()
plt.pause(0.01)

# vertical section
l,b,w,h = axs[0].get_position().bounds
axs[2] = fig.add_axes((l+w+0.01,b,.2,h))

# some customizations (called on the axes of the section)
title2_str = 'Section at lon=%.1f' % 0
t2 = axs[2].set_title(title2_str)
# ax.set_xlabel('Level (hPa)')
# ax.invert_xaxis()
axs[2].set_xlabel('Altitude (km)')
axs[2].yaxis.tick_right()
axs[2].yaxis.set_label_position('right')
axs[2].set_ylabel('Latitude (deg)')

# blank data for initiating contours
blank = np.array(np.ones((2,2), dtype=float))

# plot filled contour for wmap(lon,lat)
cflines = np.arange(20,100,10)
cmap = plt.cm.get_cmap('BuPu')
cf1 = axs[0].contourf(blank, blank, blank, cflines, cmap=cmap)
# contour lines for hmap(lon,lat) and pmap(lon,lat)
cslines1 = np.arange(7000, 11000, 100)
cs11 = axs[0].contour(blank, blank, blank, cslines1, colors='k', linewidths=1.0, linestyles='solid')
cs12 = axs[0].contour(blank, blank, blank, np.arange(870,1013,2),colors='gray', linewidths=1.0, linestyles='dashed')
cs13 = axs[0].contour(blank, blank, blank, np.arange(1014,1085,2), colors='gray', linewidths=1.0, linestyles='solid')

# plot filled contour lines for wsec(level, lat)
cf2 = axs[2].contourf(blank, blank, blank, cflines, cmap=cmap)
# plot line of hgt of 300hPa surface at lon
l3, = axs[2].plot([], [], 'k-', linewidth=1.0)
cslines2 = np.arange(100, 600, 100)
cs2 = axs[2].contour(blank, blank, blank, cslines2, colors='b', linewidths=1.0, linestyles='solid')

# eventually will try determine polar jet stream (pjs) and subtropical js (stjs)
# plot jet stream locations on map
jsmap, = axs[0].plot([],[], 'ro', markersize=6)
# and on vertical section
jsvec, = axs[2].plot([],[], 'ro', markersize=6)

def update_section_plot(val):
    # when lon slider changes
    global js,jsvec,l3,cf1,cf2,cs11,cs12,cs13,cs2   
    dtidx = int(sdt.val)
    lonidx = int(slon.val)

    # need to subset js for this longitude
    thislon = np.where( d['lon'][js[:,JSLON]] == d['lon'][lonidx] )
    which_lats = js[thislon,JSLAT]
    which_lvls = js[thislon,JSLVL]
    yy = d['lat'][which_lats]
    jsvec.set_ydata(yy)

    # determine ht at these lats for jet stream locatios
    ht = metpy.calc.add_pressure_to_height(d['ht_std'][which_lvls], d['pdiff'][dtidx,which_lats,lonidx].squeeze())
    xx = ht.m
    jsvec.set_xdata(xx)

    # all standard press hts mesh (dot.m is metpy way of getting array)
    vlats, lvls = np.meshgrid(d['lat'], d['level'])
    vlats, hts_std = np.meshgrid(d['lat'], d['ht_std'].m)
    # add units for metpy.calc
    hts_std = hts_std * d['ht_std'].units
    # compute new hts based on adding pdiff to standard heights
    hts = metpy.calc.add_pressure_to_height(hts_std, d['pdiff'][dtidx,:,lonidx].squeeze())
    wsec = d['wspd'][dtidx,:,:,lonidx].squeeze()
    # move the lon line and change title
    l1.set_xdata([ d['lon'][lonidx], d['lon'][lonidx]])
    title2_str = 'Section at lon=%.1f' % d['lon'][lonidx]
    t2.set_text(title2_str)
    # remove previous filled contours
    for tp in cf2.collections:
        tp.remove()
    # plot new contours
    # cf2 = ax.contourf(lvls, vlats, wsec, cflines, cmap=cmap)
    cf2 = axs[2].contourf(hts, vlats, wsec, cflines, cmap=cmap)
    # cf2 = axs[2].contour(hts, vlats, wsec, cflines, cmap=cmap)

    # pick data of 300hPa surface from hgt
    (lev300,) = (d['level']==300).nonzero()
    hsec = d['hgt'][dtidx,lev300,:,lonidx].squeeze()
    # 
    l3.set_xdata(hsec)
    l3.set_ydata(d['lat'])
    
    hsec = d['hgt'][dtidx,:,:,lonidx].squeeze()
    # remove previous contours and labels
    for tp in cs2.collections:
        tp.remove()
    for lb in cs2.clabel():
        lb.remove()
    # plot new contours, pressure levels
    # cs2 = ax.contour(lvls, vlats, lvls, cslines, colors='k', linewidths=1.0, linestyles='solid')
    # contour lines for hsec is altitude (height) of constant pressure surface (level)
    cs2 = axs[2].contour(hsec, vlats, lvls, cslines2, colors='b', linewidths=1.0, linestyles='solid')
    cs2_lab = axs[2].clabel(cs2, fontsize=8, inline=1, inline_spacing=10, fmt='%i',
                        rightside_up=False, use_clabeltext=True)    

    plt.draw()

def update_both_plot(val):
    # when dt slider changes
    global js,jsmap,l3,cf1,cf2,cs11,cs12,cs13,cs2
    dtidx = int(sdt.val)
    lonidx = int(slon.val)

    # find jet stream locations each time step
    js = find_jets(d,dtidx,lm)
    jsmap.set_ydata(d['lat'][js[:,JSLAT]])
    jsmap.set_xdata(d['lon'][js[:,JSLON]])
    
    dt_str = d['dt'][dtidx].strftime("%Y_%m_%d_%H%M")
    t1.set_text(dt_str)
    lons, lats = np.meshgrid(d['lon'], d['lat'])
    # avg wspd between 100 and 400 hPa levels 
    (lev14,) = ((d['level']>=100) & (d['level']<=400)).nonzero()
    wmap = np.mean(d['wspd'][dtidx,lev14,:,:], axis=0)
    # pick 300 hPa level of hgt
    (lev300,) = (d['level']==300).nonzero()
    hmap = d['hgt'][dtidx,lev300,:,:].squeeze()
    pmap = d['msl'][dtidx,:,:].squeeze()
    # remove previous all previous contours and labels
    c = cf1.collections
    c.extend(cs11.collections)
    c.extend(cs12.collections)
    c.extend(cs13.collections)
    for tp in c:
        tp.remove()
    l = cf1.clabel()
    l.extend(cs11.clabel())
    l.extend(cs12.clabel())
    l.extend(cs13.clabel())
    for lb in l:
        lb.remove()
    # plot filled contour for wmap(lon,lat)
    cf1 = axs[0].contourf(lons, lats, wmap, cflines, cmap=cmap)
    # contour lines for hmap(lon,lat) and pmap(lon,lat)
    cs11 = axs[0].contour(lons, lats, hmap, cslines1, colors='k', linewidths=1.0, linestyles='solid')
    cs11_lab = axs[0].clabel(cs11, fontsize=8, inline=1, inline_spacing=10, fmt='%i',
                             rightside_up=True, use_clabeltext=True)
    # contour lines for pmap(lon,lat) (low pmap<1013 dashed) (high pmap>1013 solid)
    # ever recorded lowest 870 hPa (typhoon), highest 1085 hPa
    cs12 = axs[0].contour(lons, lats, pmap, np.arange(870,1013,2),colors='gray', linewidths=1.0, linestyles='dashed')
    cs12_lab = axs[0].clabel(cs12, fontsize=8, inline=1, inline_spacing=10, fmt='%i',
                             rightside_up=True, use_clabeltext=True)
    cs13 = axs[0].contour(lons, lats, pmap, np.arange(1014,1085,2), colors='gray', linewidths=1.0, linestyles='solid')
    cs13_lab = axs[0].clabel(cs13, fontsize=8, inline=1, inline_spacing=10, fmt='%i',
                             rightside_up=True, use_clabeltext=True)
    # plt.draw()
    update_section_plot(val)

def prev_lon(val):
    lonidx = int(slon.val)
    slon.set_val(lonidx-1)

def next_lon(val):
    lonidx = int(slon.val)
    slon.set_val(lonidx+1)

def prev_dt(val):
    dtidx = int(sdt.val)
    sdt.set_val(dtidx-1)

def next_dt(val):
    dtidx = int(sdt.val)
    sdt.set_val(dtidx+1)

def local_max_num_peaks(val):
    global lm
    lm['num_peaks']=int(eval(val))
    update_both_plot(val)

def local_max_min_distance(val):
    global lm
    lm['min_distance']=int(eval(val))
    update_both_plot(val)

def local_max_exclude_border(val):
    global lm
    lm['exclude_border']=int(eval(val))
    update_both_plot(val)

def local_max_threshold_abs(val):
    global lm
    lm['threshold_abs']=float(eval(val))
    update_both_plot(val)

def toggle_jet_stream(val):
    global jsmap, jsvec
    jsmap.set_visible(not jsmap.get_visible())
    jsvec.set_visible(not jsvec.get_visible())
    plt.draw()
    

# outer grid to frame inner grid of gui, 
# use the object handle of figure (fig) and method add_gridspec
ogs = fig.add_gridspec(5,3, left=0.1, right=0.95,  top=0.95, bottom=0.05)
# otherwise this direct call in jupyter-notebooks put the grid and widgets in new figure
# ogs = gs.GridSpec(4,3, left=0.1, right=0.95,  top=0.95, bottom=0.05)

# use top row of ogs for inner grids
# ogs[0,0] for peak_local_max inputs
# ogs[0,1] for lon and dt sliders
# ogs[0,2] for next and prev button sets


igs = gs.GridSpecFromSubplotSpec(4,2,subplot_spec=ogs[0,0], hspace=0.2)
# local_peak_max input parameters
# num_peaks
text_np = TextBox(fig.add_subplot(igs[0,1], title='Local Peak Max'), 'num_peaks', initial=str(lm['num_peaks']))
text_np.on_submit(local_max_num_peaks)
# min_distance (and dilation of max_filter)
text_md = TextBox(fig.add_subplot(igs[1,1]), 'min_distance', initial=str(lm['min_distance']))
text_md.on_submit(local_max_min_distance)
# exclude_border 
text_exb = TextBox(fig.add_subplot(igs[2,1]), 'exclude_border', initial=str(lm['exclude_border']))
text_exb.on_submit(local_max_exclude_border)
# threshold_abs
text_thresh = TextBox(fig.add_subplot(igs[3,1]), 'threshold (m/sec)', initial=str(lm['threshold_abs']))
text_thresh.on_submit(local_max_threshold_abs)


igs = gs.GridSpecFromSubplotSpec(4,1,subplot_spec=ogs[0,1], hspace=0.2)
# Longitude slider
# use the object handle of figure (fig) and method add_subplot to add
axlon = fig.add_subplot(igs[0])
slon = Slider(axlon, 'Long', 0, 100, valinit=0, valfmt='%d')
slon.on_changed(update_section_plot)
# Date slider
axdt = fig.add_subplot(igs[1])
sdt = Slider(axdt, 'Date', 0, 31*4, valinit=0, valfmt='%d')
sdt.on_changed(update_both_plot)
# JS hide/show
axcheck = fig.add_subplot(igs[2:])
# cjs = CheckButtons(axcheck, ['Show/Hide JS'], [jsmap.get_visible()])
cjs = Button(axcheck, 'Show/Hide JS')
cjs.on_clicked(toggle_jet_stream)

igs = gs.GridSpecFromSubplotSpec(4,4,subplot_spec=ogs[0,2], hspace=0.2)
# Longitude prev button
axlonprev = fig.add_subplot(igs[0,0])
blonprev = Button(axlonprev, '<')
blonprev.on_clicked(prev_lon)
# Longitude next button
axlonnext = fig.add_subplot(igs[0,1])
blonnext = Button(axlonnext, '>')
blonnext.on_clicked(next_lon)

# Date prev button
axdtprev = fig.add_subplot(igs[1,0])
bdtprev = Button(axdtprev, '<')
bdtprev.on_clicked(prev_dt)
# Date next button
axdtnext = fig.add_subplot(igs[1,1])
bdtnext = Button(axdtnext, '>')
bdtnext.on_clicked(next_dt)


def init_plot():
    """ initialize plots, finish setting up, and set slider limits
    """
    global js,jsmap,jsvec,cf1,cf2,cs11,cs12,cs13,cs2
    dtidx = 0
    lonidx = 65 # start lon on 75W

    dt_str = d['dt'][dtidx].strftime("%Y_%m_%d_%H%M")
    t1.set_text(dt_str)

    vsec_str = 'Section at lon=%.1f' % d['lon'][lonidx]
    t2.set_text(vsec_str)

    slon.valinit = lonidx
    slon.valmin = 0
    slon.valmax = len(d['lon'])-1
    slon.valstep = 1

    sdt.valinit = dtidx
    sdt.valmin = 0
    sdt.valmax = len(d['dt'])-1

    update_both_plot(0)

    # plot map adn set up colorbar
    # draw colorbar
    cb = fig.colorbar(cf1, cax=axs[1], orientation='horizontal') 
    cb.set_label('Wind Speed (m/sec)')


if len(sys.argv)==2:
    yyyy_mm = sys.argv[1]
else:
    yyyy_mm = '2018_01'

BB['dt'] = find_months(yyyy_mm)

# input path of netcdf files
# local data
# indir = os.path.join('/data', 'era5', 'test')
# d = get_data(indir, BB)

# use data on dap server
dapdir = 'http://whewell.marine.unc.edu/dods/era5/test'
d = get_data(dapdir, BB)

init_plot()
plt.draw()
