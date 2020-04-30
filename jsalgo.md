### Jet Stream Characterization

- Find maximum wind speeds in upper troposhere
- Apply further limitations when mulitple peaks are found

#### Choosing Maximum Windspeeds

One main goal is to identify the location (longitude, latitude, and altitude) of peak winds with time to identify the variable path of the jet streams. By using an image processing method called "Local Maxima Detection," the coordinates of maxima windspeeds in 2D (latitude and altitude) can be determined for each longitude and each time step.  This method efficiently automates the process to analyze decades of atmospheric reanalysis data for jet stream characteristics. 

We use the Python function `peak_local_max` available from the [*scikit-image*](https://scikit-image.org/) open-source library to implement the "Local Maxima Detection" method.

A maximum filter is used for finding local maxima. This operation dilates the original image and merges neighboring local maxima closer than the size of the dilation. Locations where the original image is equal to the dilated image are returned as local maxima. This [example](https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_peak_local_max.html) of the `peak_local_max` function demostrates how it works.

- Change parameters under "Local Maxima Detection" to change aspects of how peaks are identified by `peak_local_max`.

| Syntax | Default | Description |
|-----------:|:--------:|:-----------|
| `num_peaks` | `   4   ` | Maximum number of peaks to pick in the image |
| `min_distance` | `  3    ` | Dilation factor or minimum number of pixels separating peaks. |
| `exclude_border` | `   0   ` | Distance from the border to exclude finding peaks.  If 0, then peak may be included if on the border |
| `threshold` | `   40  ` | Minimum intensity of peaks (m/s) |

#### Further Peak Limitations

The automated process sometimes finds additional peaks that are not representative of the true jet core. Tuning the above parameters can help, but further limitations are required.  There are two additional criteria:

1. When there is more than one peak above the `threshold` (40 m/s default) contained within the same 30 m/s contour, the maximum peak is retained.  
2. Also, only positive zonal winds (eastward) are retained.

We use the `findContours()` and `pointPolygonTest()` functions from the [Open Source Computer Vision (OpenCV) Python Library](https://docs.opencv.org/master/) to test if multiple points fall within the same contour.  

