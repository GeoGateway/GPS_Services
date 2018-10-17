#!/usr/bin/env python3
# Author:  Developed for GeoGateway by Michael Heflin
# Date:  September 20, 2016
# Organization:  JPL, Caltech

from __future__ import print_function

prolog="""
**PROGRAM**
    getVelocities.py
      
**PURPOSE**
    Make kml file from most recent velocity estimates

**USAGE**
"""
epilog="""
**EXAMPLE**
    getVelocities.py --lat 33 --lon -115 --width 2 --height 2 -o velocity.kml
               
**COPYRIGHT**
    | Copyright 2016, by the California Institute of Technology
    | United States Government Sponsorship acknowledged
    | All rights reserved

**AUTHORS**
    | Developed for GeoGateway by Michael Heflin
    | Jet Propulsion Laboratory
    | California Institute of Technology
    | Pasadena, CA, USA
"""

# Import modules
import os
import sys
import math
import argparse
import subprocess
import urllib.request

def runCmd(cmd):
    '''run a command'''

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,executable='/bin/bash')
    (out, err) = p.communicate()
    if p.returncode != 0:
        raise UserWarning('failed to run {}\n{}\n'.format(cmd.split()[0],
            err))
    return out

def _getParser():
    parser = argparse.ArgumentParser(description=prolog,epilog=epilog,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-o', action='store', dest='output',required=True,help='output kml file')
    parser.add_argument('--lat', action='store', dest='lat',required=True,help='center latitude in degrees')
    parser.add_argument('--lon', action='store', dest='lon',required=True,help='center longitude in degrees')
    parser.add_argument('--width', action='store', dest='width',required=True,help='width in degrees')
    parser.add_argument('--height', action='store', dest='height',required=True,help='height in degrees')
    parser.add_argument('--scale', action='store', dest='scale',required=False,help='scale for drawing estimates, default is 320 mm/yr/deg')
    parser.add_argument('--ref', action='store', dest='ref',required=False,help='reference site')
    parser.add_argument('-e', action='store_true',dest='eon',required=False,help='include error bars')
    parser.add_argument('--minm', action='store_true',dest='mon',required=False,help='minimize marker size')
    parser.add_argument('--vabs', action='store_true',dest='vabs',required=False,help='display absolute verticals')
    return parser

def main():

    # Read command line arguments
    parser = _getParser()
    results = parser.parse_args()

    # Set bounds
    latmin = float(results.lat) - float(results.height)/2
    latmax = float(results.lat) + float(results.height)/2
    lonmin = float(results.lon) - float(results.width)/2
    lonmax = float(results.lon) + float(results.width)/2

    # Set scale
    scale = 320 
    if (results.scale != None):
        scale = float(results.scale)

    # Set marker size
    if (results.mon == True):
        msize = 0.2
    else:
        msize = 0.5

    # Set reference site
    refsite = 'NONE'
    if (results.ref != None):
        refsite = results.ref

    # Read table of positions and velocities
    response1 = urllib.request.urlopen('https://sideshow.jpl.nasa.gov/post/tables/table2.html')
    lines = response1.read().decode('utf-8').splitlines()

    # Set reference values
    rlat = 0
    rlon = 0
    rrad = 0
    for i in range(0,len(lines)):
        test = lines[i].split()
        if (len(test) == 8):
            if ((test[1] == 'POS') & (test[0] == refsite)):
                next = lines[i+1].split()
                rlat = float(next[2])
                rlon = float(next[3])
                rrad = float(next[4])

    # Start kml file
    outFile1 = open(results.output+'_horizontal.kml','w')
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>",file=outFile1)
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">",file=outFile1)
    print(" <Folder>",file=outFile1)

    # Start kml file
    outFile2 = open(results.output+'_vertical.kml','w')
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>",file=outFile2)
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">",file=outFile2)
    print(" <Folder>",file=outFile2)

    # Start txt file
    outFile3 = open(results.output+'_table.txt','w')
    print("Site          Lon          Lat      Delta E      Delta N      Delta V      Sigma E      Sigma N      Sigma V",file=outFile3)

    # Add markers and vectors
    for i in range(0,len(lines)):
        test = lines[i].split()
        if (len(test) == 8):
            if (test[1] == 'POS'):
                lon = float(test[3])
                lat = float(test[2])
                next = lines[i+1].split()
                vlon = float(next[3])
                vlat = float(next[2])
                vrad = float(next[4])
                slon = float(next[6])
                slat = float(next[5])
                srad = float(next[7])
                if ((lon > lonmin) & (lon < lonmax) & (lat > latmin) & (lat < latmax)):

                    # Subtract reference values
                    vlon = vlon-rlon
                    vlat = vlat-rlat
                    vrad = vrad-rrad
                    if (results.vabs == True):
                        vrad = vrad+rrad

                    # Set marker color
                    if (test[0] == refsite):
                        mcolor = 'FF0000FF'
                    else:
                        mcolor = 'FF78FF78'

                    # Draw markers
                    print("  <Placemark>",file=outFile1)
                    print("   <description><![CDATA[",file=outFile1)
                    print("    <a href=\"https://sideshow.jpl.nasa.gov/post/links/{:s}.html\">".format(test[0]),file=outFile1)
                    print("     <img src=\"https://sideshow.jpl.nasa.gov/post/plots/{:s}.jpg\" width=\"300\" height=\"300\">".format(test[0]),file=outFile1)
                    print("    </a>",file=outFile1)
                    print("   ]]></description>",file=outFile1)
                    print("   <Style><IconStyle>",file=outFile1)
                    print("    <color>{:s}</color>".format(mcolor),file=outFile1)
                    print("    <scale>{:f}</scale>".format(msize),file=outFile1)
                    print("    <Icon><href>https://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>",file=outFile1)
                    print("   </IconStyle></Style>",file=outFile1)
                    print("   <Point>",file=outFile1)
                    print("    <coordinates>",file=outFile1)
                    print("     {:f},{:f},0".format(lon,lat),file=outFile1)
                    print("    </coordinates>",file=outFile1)
                    print("   </Point>",file=outFile1)
                    print("  </Placemark>",file=outFile1)

                    # Draw markers
                    print("  <Placemark>",file=outFile2)
                    print("   <description><![CDATA[",file=outFile2)
                    print("    <a href=\"https://sideshow.jpl.nasa.gov/post/links/{:s}.html\">".format(test[0]),file=outFile2)
                    print("     <img src=\"https://sideshow.jpl.nasa.gov/post/plots/{:s}.jpg\" width=\"300\" height=\"300\">".format(test[0]),file=outFile2)
                    print("    </a>",file=outFile2)
                    print("   ]]></description>",file=outFile2)
                    print("   <Style><IconStyle>",file=outFile2)
                    print("    <color>{:s}</color>".format(mcolor),file=outFile2)
                    print("    <scale>{:f}</scale>".format(msize),file=outFile2)
                    print("    <Icon><href>https://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>",file=outFile2)
                    print("   </IconStyle></Style>",file=outFile2)
                    print("   <Point>",file=outFile2)
                    print("    <coordinates>",file=outFile2)
                    print("     {:f},{:f},0".format(lon,lat),file=outFile2)
                    print("    </coordinates>",file=outFile2)
                    print("   </Point>",file=outFile2)
                    print("  </Placemark>",file=outFile2)

                    # Draw vectors 
                    print("  <Placemark>",file=outFile1)
                    print("   <Style><LineStyle>",file=outFile1)
                    print("    <color>FF007800</color>",file=outFile1)
                    print("    <width>2</width>",file=outFile1)
                    print("   </LineStyle></Style>",file=outFile1)
                    print("   <LineString>",file=outFile1)
                    print("   <coordinates>",file=outFile1)
                    print("   {:f},{:f},0".format(lon,lat),file=outFile1)
                    print("   {:f},{:f},0".format(lon+vlon/scale/math.cos(lat*math.pi/180.),lat+vlat/scale),file=outFile1)
                    print("    </coordinates>",file=outFile1)
                    print("   </LineString>",file=outFile1)
                    print("  </Placemark>",file=outFile1)

                    # Draw sigmas
                    if (results.eon == True):
                        print("  <Placemark>",file=outFile1)
                        print("   <Style>",file=outFile1)
                        print("    <LineStyle>",file=outFile1)
                        print("     <color>FF000000</color>",file=outFile1)
                        print("     <width>2</width>",file=outFile1)
                        print("    </LineStyle>",file=outFile1)
                        print("    <PolyStyle>",file=outFile1)
                        print("     <color>FF000000</color>",file=outFile1)
                        print("     <fill>0</fill>",file=outFile1)
                        print("    </PolyStyle>",file=outFile1)
                        print("   </Style>",file=outFile1)
                        print("   <Polygon>",file=outFile1)
                        print("    <outerBoundaryIs>",file=outFile1)
                        print("     <LinearRing>",file=outFile1)
                        print("      <coordinates>",file=outFile1)

                        theta = 0
                        for k in range(0,31):
                            angle = k/30*2*math.pi
                            elon = slon*math.cos(angle)*math.cos(theta)-slat*math.sin(angle)*math.sin(theta)
                            elat = slon*math.cos(angle)*math.sin(theta)+slat*math.sin(angle)*math.cos(theta)
                            elon = (elon+vlon)/scale/math.cos(lat*math.pi/180.)
                            elat = (elat+vlat)/scale 
                            print("      {:f},{:f},0".format(lon+elon,lat+elat),file=outFile1)

                        print("      </coordinates>",file=outFile1)
                        print("     </LinearRing>",file=outFile1)
                        print("    </outerBoundaryIs>",file=outFile1)
                        print("   </Polygon>",file=outFile1)
                        print("  </Placemark>",file=outFile1)

                    # Set circle color
                    if (vrad > 0):
                        lcolor = 'FF0000FF'
                        pcolor = '7F0000FF'
                    else:
                        lcolor = 'FFFF0000'
                        pcolor = '7FFF0000'

                    # Draw circle size proportional to vertical
                    print("  <Placemark>",file=outFile2)
                    print("   <Style>",file=outFile2)
                    print("    <LineStyle>",file=outFile2)
                    print("     <color>{:s}</color>".format(lcolor),file=outFile2)
                    print("     <width>1</width>",file=outFile2)
                    print("    </LineStyle>",file=outFile2)
                    print("    <PolyStyle>",file=outFile2)
                    print("     <color>{:s}</color>".format(pcolor),file=outFile2)
                    print("     <fill>1</fill>",file=outFile2)
                    print("    </PolyStyle>",file=outFile2)
                    print("   </Style>",file=outFile2)
                    print("   <Polygon>",file=outFile2)
                    print("    <outerBoundaryIs>",file=outFile2)
                    print("     <LinearRing>",file=outFile2)
                    print("      <coordinates>",file=outFile2)

                    theta = 0
                    for k in range(0,31):
                        angle = k/30*2*math.pi
                        elon = vrad*math.cos(angle)*math.cos(theta)-vrad*math.sin(angle)*math.sin(theta)
                        elat = vrad*math.cos(angle)*math.sin(theta)+vrad*math.sin(angle)*math.cos(theta)
                        elon = (elon+0)/scale/math.cos(lat*math.pi/180.)
                        elat = (elat+0)/scale 
                        print("      {:f},{:f},0".format(lon+elon,lat+elat),file=outFile2)

                    print("      </coordinates>",file=outFile2)
                    print("     </LinearRing>",file=outFile2)
                    print("    </outerBoundaryIs>",file=outFile2)
                    print("   </Polygon>",file=outFile2)
                    print("  </Placemark>",file=outFile2)

                    # Make table
                    print("{:s} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f}".format(
                    test[0],lon,lat,vlon,vlat,vrad,slon,slat,srad),file=outFile3)

    # Finish files
    print(" </Folder>",file=outFile1)
    print("</kml>",file=outFile1)
    outFile1.close()
    print(" </Folder>",file=outFile2)
    print("</kml>",file=outFile2)
    outFile2.close()
    outFile3.close()

if __name__ == '__main__':
    main()
