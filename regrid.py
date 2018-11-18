import iris
import iris_sample_data
import iris_grib
import sys
import pyproj as proj
#ds = xr.open_dataset('/home/awips/python-awips/ups/20181110_1600.nc',decode_times=False,decode_cf=False,mask_and_scale=False)

data = '/home/awips/python-awips/ups/20181110_1600.nc'
path = iris.sample
#air_temp = iris.load_cube('/home/awips/python-awips/ups/latest.nc')
#print(air_temp)
#scheme = iris.analysis.Linear(extrapolation_mode='mask')
#new_grid = air_temp.regrid(air_temp, scheme)



