### Jet Stream Characterization

- Find maximum wind speeds in upper troposhere, using 4D ERA5 data.
- Apply further limitations when mulitple peaks are found

#### Choosing Maximum Windspeeds

To identify the jet stream(s), globally or regionally, the location (longitude, latitude, and altitude or pressure level) of peak winds with time need to be identified to plot the variable path(s).  For 'jsviz', we adopt a similar strategy used by Manney et al. [1] and Rikus [2] to determine jet stream positions.  This methodology evaluates maximum windpeeds from reanalysis data along each longitudinal slice through the upper atmosphere.  

The region of `jsviz` is centered on North America (0-80 deg N and 140-50 deg W), every 6 hours but could be expanded to wider extents in time and space and/or higher resolution. Furthermore, several data fields, primarily the magnitude of the windspeed (wspd), geopotential heigt (hgt) and altitude, are computed from the ERA5 base data using [MetPy](https://unidata.github.io/MetPy/latest/) [3], a collection of tools for calculating derived variables of weather data and managing their scientific units. 

By using an image processing method called "Local Maxima Detection," the coordinates of maxima windspeeds in 2D (latitude and altitude/pressure) can be determined for each longitude and each time step.  This method efficiently automates the process to analyze multiple years or decades of atmospheric reanalysis data for jet stream characteristics. We use the Python function `peak_local_max` available from the [*scikit-image*](https://scikit-image.org/) [4], an open-source library of algorithms for image processing, to implement the "Local Maxima Detection" method. A similar image analysis package is employed by Rinkus [2].

For each image, or 2D field of windspeed, a maximum filter is used for finding local maxima. This operation dilates the original image and merges neighboring local maxima closer than the size of the dilation. Locations where the original image is equal to the dilated image are returned as local maxima.  [An example](https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_peak_local_max.html) from the scikit-image documentation demostrates how the `peak_local_max` function works.

Input parameters used by `peak_local_max` function change aspects of how peaks are identified.  In the `jsviz` tool, a set of dominant parameters are provided under the label "Local Maxima Detection". Default values are set but can be changed to visualize and tune how jet stream positions are found.

| Syntax | Default | Description |
|-----------:|:--------:|:-----------|
| `num_peaks` | `   4   ` | Maximum number of peaks to pick in the image |
| `min_distance` | `  3    ` | Dilation factor or minimum number of pixels separating peaks. |
| `exclude_border` | `   0   ` | Distance from the border to exclude finding peaks.  If 0, then peak may be included if on the border. |
| `threshold` | `   40  ` | Minimum intensity of peaks (m/s) |

#### Further Peak Limitations

The `peak_local_max` function sometimes finds additional peaks that may or may not represent jet cores. Tuning the above parameters can help, but further limitations are required.  There are two additional criteria applied here to determine jet stream position:

1. When there is more than one peak above the `threshold` (40 m/s default) contained within the same 30 m/s contour, the maximum peak is retained.  
2. Peaks with positive zonal winds (eastward) only are retained.

We use the `findContours()` and `pointPolygonTest()` functions from the [Open Source Computer Vision (OpenCV) Python Library](https://docs.opencv.org/master/) [5] to test if multiple points fall within the same contour.

### References

[1] Manney GL, Hegglin MI, Daffer WH et al, 2011: Jet characterization in the upper troposphere/lower stratosphere (UTLS): applications to climatology and transport studies. Atmos Chem Phys 11:1835–1889. doi:10.5194/acpd-11-1835-2011.

[2] Rikus, L., 2015: A simple climatology of westerly jet streams in global reanalysis datasets. Part 1: Mid-latitude upper tropospheric jets. Climate Dyn., doi:10.1007/ s00382-015-2560-y.

[3] May, R. M., Arms, S. C., Marsh, P., Bruning, E., Leeman, J. R., Goebbert, K., Thielen, J. E., and Bruick, Z., 2020: MetPy: A Python Package for Meteorological Data. Version 0.12.1.post2, Unidata, Accessed 21 April 2020. [Available online at https://github.com/Unidata/MetPy.] doi:10.5065/D6WW7G29.

[4] Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image contributors, 2014: scikit-image: Image processing in Python. PeerJ 2:e453 https://doi.org/10.7717/peerj.453

[5] Bradski, G., 2000: The OpenCV Library. Dr. Dobb's Journal of Software Tools.
