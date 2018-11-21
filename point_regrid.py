import sys

import cartopy.crs as ccrs
from cf_units import Unit
import iris
import iris_grib
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

def create_1d_coord(lower, upper, no, *args, **kwargs):
    bounds_pre = np.linspace(lower, upper, no)
    bounds = np.stack([bounds_pre[:-1],
                       bounds_pre[1:]],
                      axis=-1)
    points = bounds.mean(axis=-1)
    #print(bounds)
    #print(points)
    coord = iris.coords.DimCoord(
        points,
        *args,
        bounds=bounds,
        **kwargs
    )
    return coord

def create_tgt_cube():
    no_lat = 120
    no_lon = 276
    lat = create_1d_coord(20, 50, no_lat+1,
                          'latitude',
                          long_name='latitude',
                          var_name='lat',
                          units=Unit('degrees_north'))
    lon = create_1d_coord(-131, -62, no_lon+1,
                          'longitude',
                          long_name='longitude',
                          var_name='lon',
                          units=Unit('degrees_east'),
                          circular=False)
    #timef = (tpoints, standard_name='time', long_name='time', var_name='time')
    data = np.empty((no_lat, no_lon))
    cube = iris.cube.Cube(data,
                          dim_coords_and_dims=[(lat, 0), (lon, 1)])
    return cube

"""
def create_tgt_cube():
    no_lat = 180
    no_lon = 360
    lat = create_1d_coord(-90, 90, no_lat+1,
                          'latitude',
                          long_name='latitude',
                          var_name='lat',
                          units=Unit('degrees_north'))
    lon = create_1d_coord(0, 360, no_lon+1,
                          'longitude',
                          long_name='longitude',
                          var_name='lon',
                          units=Unit('degrees_east'),
                          circular=True)
    data = np.empty((no_lat, no_lon))
    cube = iris.cube.Cube(data,
                          dim_coords_and_dims=[(lat, 0), (lon, 1)])
    return cube
"""

def get_range(coord):
    min = coord.points.min()
    max = coord.points.max()
    return (min, max)


"""
def plot_global_cube(cube):
    cube.units = Unit('degF')
    cube.convert_units('degC')
    ax = plt.subplot(1, 2, 1, projection=ccrs.PlateCarree())
    qplt.pcolormesh(cube)
    ax.coastlines()
"""

def plot_cube(cube):
    cube.units = Unit('degK')
    #cube.convert_units('degF')
    #ax = plt.subplot(1, 2, 2, projection=ccrs.Mollweide())
    proj = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=38.5,
                             false_easting=0, false_northing=0,
                             standard_parallels=(38.5, 3))
    fig = plt.figure(figsize=(8, 8), frameon=True)
    ax = fig.add_axes([0.08, 0.05, 0.8, 0.94], projection=proj)
    qplt.pcolormesh(cube, cmap='rainbow')
    ax.coastlines(resolution='10m',lw=0.3)


def main():
    filename = sys.argv[1]
    cube = iris.load_cube(filename)
    #print(cube.coord('time').points)
    print(cube)
    lat_range = get_range(cube.coord('latitude'))
    lon_range = get_range(cube.coord('longitude'))
    tgt_cube_global = create_tgt_cube()
    rgr_cube_global = cube.regrid(tgt_cube_global,
                                  iris.analysis.UnstructuredNearest())
    rgr_cube = rgr_cube_global.intersection(latitude=lat_range,
                                            longitude=lon_range)
    radius=iris.fileformats.pp.EARTH_RADIUS
    rgr_cube.coord(dimensions=[0]).coord_system=iris.coord_systems.GeogCS(radius)
    rgr_cube.coord(dimensions=[1]).coord_system=iris.coord_systems.GeogCS(radius)

    #rgr_cube.coord(axis='X').coord_system=iris.coord_systems.GeogCS(654321)
    #rgr_cube.coord(axis='Y').coord_system=iris.coord_systems.GeogCS(654321)


    #rgr_cube.coord(dimensions=[0]).coord_system
    #rgr_cube.coord(dimensions=[1]).coord_system
    #plot_global_cube(rgr_cube_global)
    t_unit = Unit('seconds since 1970-01-01 00:00:00', calendar='gregorian')
    rgr_cube.add_aux_coord(iris.coords.DimCoord(1541865240, standard_name='time', units=t_unit))
    rgr_cube.add_aux_coord(iris.coords.DimCoord(0, standard_name='forecast_period', units='hours'))
    rgr_cube.add_aux_coord(iris.coords.DimCoord(0, standard_name='height', units='m'))
    rgr_cube.data = ma.masked_invalid(rgr_cube.data)
    print(rgr_cube)
    #plot_cube(rgr_cube)


    iris.save(rgr_cube, '/home/awips/python-awips/ups/latest.grib2')
    plt.show()


if __name__ == '__main__':
    main()
