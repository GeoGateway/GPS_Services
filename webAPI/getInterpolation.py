"""
getInterpolation.py
    -- GPS Interpolation 
    -- https://github.com/GeoGateway/JupyterNotebooks/tree/master/GPS_interpolation
"""

import argparse

def _getParser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-dt', '--datatable', action='store', dest='datatable',required=True,help='data table in csv')
    parser.add_argument('-gs','--gridspaceing', action='store', dest='grid_space',required=False,help='Grid Spacing',default=0.018)
    parser.add_argument('-it','--interpolation_type', action='store', dest='interpolation_type',required=False,help='Interpolation type', 
        choices=['linear', 'gaussian', 'power','exponential', 'hole-effect', 'spherical'], default='linear')
    parser.add_argument('-az','--azimuth', action='store', dest='azimuth',required=False,help='Azimuth', default=-5)
    parser.add_argument('-ea','--elevationangle', action='store', dest='elevation',required=False,help='Elevation Angle', default=60)
    
    return parser

def main():

    # Read command line arguments
    parser = _getParser()
    results = parser.parse_args()
    getInterpolation(results)

def getInterpolation(results):
    """run interpolation"""
    print(results)

if __name__ == '__main__':
    main()
