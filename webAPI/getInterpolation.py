"""
getInterpolation.py
    -- GPS Interpolation 
    -- https://github.com/GeoGateway/JupyterNotebooks/tree/master/GPS_interpolation
"""

import argparse
from configparser import Interpolation
import re

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
    print(gps_df)

if __name__ == '__main__':
    main()
