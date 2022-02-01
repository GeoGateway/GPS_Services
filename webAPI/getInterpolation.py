"""
getInterpolation.py
    -- GPS Interpolation 
    -- https://github.com/GeoGateway/JupyterNotebooks/tree/master/GPS_interpolation
    -- requirements: pykrige
"""

import math
import argparse
import matplotlib.pyplot as plt
import pandas as pd

from load_gps_data import load_gps_data
from gps_interpolation import interpolate, create_grid, reshape_and_create_df

def _getParser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-dt', '--datatable', action='store', dest='datatable',required=True,help='data table in csv')
    parser.add_argument('-gs','--gridspaceing', action='store', dest='grid_space',required=False,help='Grid Spacing',default=0.018)
    parser.add_argument('-it','--interpolation_type', action='store', dest='interpolation_type',required=False,help='Interpolation type', 
        choices=['linear', 'gaussian', 'power','exponential', 'hole-effect', 'spherical'], default='linear')
    parser.add_argument('-az','--azimuth', action='store', dest='azimuth',required=False,help='Azimuth', default=-5)
    parser.add_argument('-ea','--elevation', action='store', dest='elevation',required=False,help='Elevation Angle', default=60)
    
    return parser

def main():

    # Read command line arguments
    parser = _getParser()
    results = parser.parse_args()
    getInterpolation(results)

def getInterpolation(results):
    """run interpolation"""
    print(results)

    datatable = results.datatable
    grid_space = results.grid_space
    interpolation_type = results.interpolation_type
    azimuth = results.azimuth
    elevation = results.elevation

    # load data from data table
    gps_df = load_gps_data(datatable)
    deltas = gps_df[['Delta E', 'Delta N', 'Delta V']]

    interpolated_values = interpolate(
        gps_df['Lon'],
        gps_df['Lat'],
        grid_spacing=grid_space,
        model=interpolation_type,
        **deltas)

    losd = to_los_disp(interpolated_values['Delta E'], interpolated_values['Delta N'],
                       interpolated_values['Delta V'], elevation=elevation, azimuth=azimuth)
    interpolated_values['LOS Displacement'] = losd

    collist = ['Delta N', 'Delta E', 'Delta V', 'LOS Displacement']
    for entry in collist:
        create_contour_overlay(
            interpolated_values['Lon'], interpolated_values['Lat'], interpolated_values[entry])


def to_los_disp(ux, uy, uv, azimuth=-5, elevation=60):
    g = [math.sin(azimuth)*math.cos(elevation), math.cos(azimuth)
         * math.cos(elevation), math.sin(elevation)]
    losd = (g[0]*ux + g[1]*uy + g[2]*uv)/5.0
    return losd

def create_contour_overlay(Lon, Lat, Z):
    """
    input pandas df columns with X, Y, Z
    Saves png of tricontour. I switched to this because
    it allowed for much faster load times than trying to plot
    color coated points on folium.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.tricontourf(Lon, Lat, Z, cmap="seismic")
    # everything below this is to remove white space and axis from plot
    # in order to save the image and plot on map properly.
    # there may be some distortion due to no geo correction in mpl but I am not sure
    # since the interpolation itself handles geo coordinates and corrections
    fig.frameon = False
    fig.gca().xaxis.set_major_locator(plt.NullLocator())
    fig.gca().yaxis.set_major_locator(plt.NullLocator())
    ax.set_axis_off()
    plt.close(fig)
    fig.savefig(f"contour_of_{Z.name}.png", bbox_inches="tight", pad_inches=0)

if __name__ == '__main__':
    main()
