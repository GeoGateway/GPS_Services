"""
getInterpolation.py
    -- GPS Interpolation 
    -- https://github.com/GeoGateway/JupyterNotebooks/tree/master/GPS_interpolation
    -- requirements: pykrige
"""

import os, sys
import math
import argparse
import shutil
import numpy as np
import matplotlib.pyplot as plt

from load_gps_data import load_gps_data
from gps_interpolation import interpolate, create_grid, reshape_and_create_df

def _getParser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-dt', '--datatable', action='store', dest='datatable',required=True,help='data table in csv')
    parser.add_argument('-gs','--gridspacing', action='store', dest='gridspacing',required=False,help='Grid Spacing',default=0.018)
    parser.add_argument('-it','--interpolationtype', action='store', dest='interpolationtype',required=False,help='Interpolation type', 
        choices=['linear', 'gaussian', 'power','exponential', 'hole-effect', 'spherical'], default='linear')
    parser.add_argument('-az','--azimuth', action='store', dest='azimuth',required=False,help='Azimuth', default=-5)
    parser.add_argument('-ea','--elevation', action='store', dest='elevation',required=False,help='Elevation Angle', default=60)
    parser.add_argument('-z', '--zip', action='store_true',dest='zip',required=False,help='create zip file')
    
    return parser

def main():

    # Read command line arguments
    parser = _getParser()
    results = parser.parse_args()
    getInterpolation(results)

def getInterpolation(results):
    """run interpolation"""
 
    curdir = os.getcwd()
    
    datatable = os.path.basename(results.datatable)
    wkdir = os.path.dirname(results.datatable)
    if os.path.exists(wkdir):
        os.chdir(wkdir)
    gridspacing = float(results.gridspacing)
    interpolationtype = results.interpolationtype
    azimuth = float(results.azimuth)
    elevation = float(results.elevation)

    # load data from data table
    gps_df = load_gps_data(datatable)
    deltas = gps_df[['Delta E', 'Delta N', 'Delta V']]

    interpolated_values = interpolate(
        gps_df['Lon'],
        gps_df['Lat'],
        grid_spacing=gridspacing,
        model=interpolationtype,
        **deltas)

    losd = to_los_disp(interpolated_values['Delta E'], interpolated_values['Delta N'],
                       interpolated_values['Delta V'], elevation=elevation, azimuth=azimuth)
    interpolated_values['LOS Displacement'] = losd

    collist = ['Delta N', 'Delta E', 'Delta V', 'LOS Displacement']
    for entry in collist:
        create_contour_overlay(
            interpolated_values['Lon'], interpolated_values['Lat'], interpolated_values[entry])

    # zip results:
    if results.zip:
        shutil.make_archive('gps_interpolation','zip')

    # get imagebounds
    lat0, lat1 = gps_df['Lat'].min(), gps_df['Lat'].max()
    lon0, lon1 = gps_df['Lon'].min(), gps_df['Lon'].max()
    imagebounds = [[lat0,lon0],[lat1,lon1]]
    os.chdir(curdir)
    
    return imagebounds

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

    imagename = Z.name.replace(" ","_")

    fig, ax = plt.subplots(nrows=1, ncols=1)
    mbp = ax.tricontourf(Lon, Lat, Z, cmap="seismic")
    # everything below this is to remove white space and axis from plot
    # in order to save the image and plot on map properly.
    # there may be some distortion due to no geo correction in mpl but I am not sure
    # since the interpolation itself handles geo coordinates and corrections
    fig.frameon = False
    fig.gca().xaxis.set_major_locator(plt.NullLocator())
    fig.gca().yaxis.set_major_locator(plt.NullLocator())
    ax.set_axis_off()
    plt.close(fig)
    fig.savefig(f"contour_of_{imagename}.png", bbox_inches="tight", pad_inches=0)
    
    # plot another one for colorbar
    # color bar need more work to get it looks good
    fig,ax = plt.subplots()
    ticks = np.linspace(Z.min(),Z.max(),5)
    cbar = plt.colorbar(mbp,ax=ax,orientation="horizontal",ticks=ticks)
    #cbar.ax.locator_params(nbins=3)
    ax.remove()
    plt.savefig(f"contour_of_{imagename}_colorbar0.png",bbox_inches='tight',transparent=False)
    plt.savefig(f"contour_of_{imagename}_colorbar.png",bbox_inches='tight',transparent=True)
    plt.close(fig)

    # create KML
    kml_template = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>{imagename}</name>
        <description></description>
        <GroundOverlay>
            <name>contour_of_{imagename}.png</name>
            <color>ccffffff</color>
            <Icon>
                <href>contour_of_{imagename}.png</href>
                <viewBoundScale>0.75</viewBoundScale>
            </Icon>
            <LatLonBox>
                <north>{north}</north>
                <south>{south}</south>
                <east>{east}</east>
                <west>{west}</west>
            </LatLonBox>
        </GroundOverlay>
        <ScreenOverlay>
            <name>Legend</name>
            <visibility>1</visibility>
            <Icon>
                <href>contour_of_{imagename}_colorbar0.png</href>
            </Icon>
            <overlayXY x="0.5" y="1" xunits="fraction" yunits="fraction"/>
            <screenXY x="0.5" y="1" xunits="fraction" yunits="fraction"/> 
            <rotationXY x="0" y="0" xunits="fraction" yunits="fraction" />
            <size x="0" y="0" xunits="fraction" yunits="fraction" />
        </ScreenOverlay>
    </Document>
</kml>"""
    lat0, lat1 = Lat.min(), Lat.max()
    lon0, lon1 = Lon.min(), Lon.max()
    kmlname = f"contour_of_{imagename}.kml"
    with open(kmlname,"w") as f:
        f.write(kml_template.format(imagename=imagename, north=lat1,south=lat0,east=lon1,west=lon0))
    
if __name__ == '__main__':
    main()
