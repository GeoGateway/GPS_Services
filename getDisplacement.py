#!/usr/bin/env python3
# Author:  Developed for GeoGateway by Michael Heflin
# Date:  September 20, 2016
# Organization:  JPL, Caltech

from __future__ import print_function

prolog="""
**PROGRAM**
    getDisplacement.py
      
**PURPOSE**
    Make kml file from displacement observed between two epochs

**USAGE**
"""
epilog="""
**EXAMPLE**
    getDisplacement.py --lat 33 --lon -115 --width 2 --height 2 -t1 2010-04-07 -t2 2010-04-09 -o displacement.kml
               
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
import time
import datetime
import calendar
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
    parser.add_argument('-t1', action='store', dest='epoch1',required=True,help='epoch1')
    parser.add_argument('-t2', action='store', dest='epoch2',required=True,help='epoch2')
    parser.add_argument('--scale', action='store', dest='scale',required=False,help='scale for offsets in mm/deg')
    parser.add_argument('--ref', action='store', dest='ref',required=False,help='reference site')
    parser.add_argument('--vertical', action='store_true', dest='vertical',required=False,help='show vertical only')
    parser.add_argument('-e', action='store_true',dest='eon',required=False,help='include error bars')
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

    # Set first epoch
    if (len(results.epoch1) == 10):
        results.epoch1 = datetime.datetime.strptime(results.epoch1,"%Y-%m-%d").strftime("%y%b%d").upper()
        ntime = time.strptime(results.epoch1,"%y%b%d")
        jtime = time.strptime("2000JAN01","%Y%b%d")
        ytime1 = float(calendar.timegm(ntime)-calendar.timegm(jtime))
        ytime1 = ytime1/(86400.*365.25)
        ytime1 = ytime1 + 2000.

    # Set second epoch
    if (len(results.epoch2) == 10):
        results.epoch2 = datetime.datetime.strptime(results.epoch2,"%Y-%m-%d").strftime("%y%b%d").upper()
        ntime = time.strptime(results.epoch2,"%y%b%d")
        jtime = time.strptime("2000JAN01","%Y%b%d")
        ytime2 = float(calendar.timegm(ntime)-calendar.timegm(jtime))
        ytime2 = ytime2/(86400.*365.25)
        ytime2 = ytime2 + 2000.

    # Read table of positions
    response1 = urllib.request.urlopen('http://sideshow.jpl.nasa.gov/post/tables/table2.html')
    lines = response1.read().decode('utf-8').splitlines()

    # Read reference series
    rlon = 0
    rlat = 0
    rrad = 0
    stop = 0
    refsite = 'NONE'
    if (results.ref != None):
        refsite = results.ref
        location = 'ftp://sideshow.jpl.nasa.gov/pub/usrs/mbh/point/'+refsite+'.series'
        request = urllib.request.Request(location)
        response2 = urllib.request.urlopen(request)
        series = response2.read().decode('utf-8').splitlines()

        # Set reference values
        scount = 0
        for j in range(0,len(series)):
            test2 = series[j].split()
            if (math.sqrt((float(test2[0])-ytime1)*(float(test2[0])-ytime1))) < 0.001:
                rlon = rlon - float(test2[1])
                rlat = rlat - float(test2[2])
                rrad = rrad - float(test2[3])
                scount = scount + 1
            if (math.sqrt((float(test2[0])-ytime2)*(float(test2[0])-ytime2))) < 0.001:
                rlon = rlon + float(test2[1])
                rlat = rlat + float(test2[2])
                rrad = rrad + float(test2[3])
                scount = scount + 1
        rlon = 1000.*rlon
        rlat = 1000.*rlat
        rrad = 1000.*rrad

        # Only use displacements computed from both epochs
        if (scount < 2):
            rlon = 0
            rlat = 0
            rrad = 0
            stop = 1
            print("Reference site has missing data!")

    # Start kml file
    outFile = open(results.output,'w')
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>",file=outFile)
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\">",file=outFile)
    print(" <Folder>",file=outFile)

    # Start txt file
    txtFile = open(results.output.partition('.')[0]+'.txt','w')
    print("Site          Lon          Lat      Delta E      Delta N      Delta V      Sigma E      Sigma N      Sigma V",file=txtFile)

    # Add markers and vectors
    for i in range(0,len(lines)):
        test = lines[i].split()
        if (len(test) == 8):
            if (test[1] == 'POS'):
                lon = float(test[3])
                lat = float(test[2])
                if ((lon > lonmin) & (lon < lonmax) & (lat > latmin) & (lat < latmax)):

                    # Read time series
                    location = 'ftp://sideshow.jpl.nasa.gov/pub/usrs/mbh/point/'+test[0]+'.series'
                    request = urllib.request.Request(location)
                    response2 = urllib.request.urlopen(request)
                    series = response2.read().decode('utf-8').splitlines()

                    # Compute displacment
                    vlon = 0
                    vlat = 0
                    vrad = 0
                    slon = 0
                    slat = 0
                    srad = 0
                    scount = 0
                    for j in range(0,len(series)):
                        test2 = series[j].split()
                        if (math.sqrt((float(test2[0])-ytime1)*(float(test2[0])-ytime1))) < 0.001:
                            vlon = vlon - float(test2[1])
                            vlat = vlat - float(test2[2])
                            vrad = vrad - float(test2[3])
                            slon = slon + float(test2[4])*float(test2[4])
                            slat = slat + float(test2[5])*float(test2[5])
                            srad = srad + float(test2[6])*float(test2[6])
                            scount = scount + 1
                        if (math.sqrt((float(test2[0])-ytime2)*(float(test2[0])-ytime2))) < 0.001:
                            vlon = vlon + float(test2[1])
                            vlat = vlat + float(test2[2])
                            vrad = vrad + float(test2[3])
                            slon = slon + float(test2[4])*float(test2[4])
                            slat = slat + float(test2[5])*float(test2[5])
                            srad = srad + float(test2[6])*float(test2[6])
                            scount = scount + 1
                    vlon = 1000.*vlon
                    vlat = 1000.*vlat
                    vrad = 1000.*vrad
                    slon = 1000.*math.sqrt(slon)
                    slat = 1000.*math.sqrt(slat)
                    srad = 1000.*math.sqrt(srad)

                    # Subtract reference values
                    vlon = vlon-rlon
                    vlat = vlat-rlat
                    vrad = vrad-rrad

                    # Only use displacements computed from both epochs
                    if ((scount >= 2) & (stop != 1)):

                        # Set marker color
                        if (test[0] == refsite):
                            mcolor = 'FF0000FF'
                        else:
                            mcolor = 'FF78FF78'

                        # Draw marker 
                        print("  <Placemark>",file=outFile)
                        print("   <description><![CDATA[",file=outFile)
                        print("    <a href=\"http://sideshow.jpl.nasa.gov/post/links/{:s}.html\">".format(test[0]),file=outFile)
                        print("     <img src=\"http://sideshow.jpl.nasa.gov/post/plots/{:s}.jpg\" width=\"300\" height=\"300\">".format(test[0]),file=outFile)
                        print("    </a>",file=outFile)
                        print("   ]]></description>",file=outFile)
                        print("   <Style><IconStyle>",file=outFile)
                        print("    <color>{:s}</color>".format(mcolor),file=outFile)
                        print("    <scale>0.50</scale>",file=outFile)
                        print("    <Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>",file=outFile)
                        print("   </IconStyle></Style>",file=outFile)
                        print("   <Point>",file=outFile)
                        print("    <coordinates>",file=outFile)
                        print("     {:f},{:f},0".format(lon,lat),file=outFile)
                        print("    </coordinates>",file=outFile)
                        print("   </Point>",file=outFile)
                        print("  </Placemark>",file=outFile)

                        # Draw vector    
                        print("  <Placemark>",file=outFile)
                        print("   <Style><LineStyle>",file=outFile)
                        print("    <color>FFB478FF</color>",file=outFile)
                        print("    <width>2</width>",file=outFile)
                        print("   </LineStyle></Style>",file=outFile)
                        print("   <LineString>",file=outFile)
                        print("   <coordinates>",file=outFile)

                        if (results.vertical == True):
                          print("   {:f},{:f},0".format(lon,lat),file=outFile)
                          print("   {:f},{:f},0".format(lon,lat+vrad/scale),file=outFile)
                        else:
                          print("   {:f},{:f},0".format(lon,lat),file=outFile)
                          print("   {:f},{:f},0".format(lon+vlon/scale,lat+vlat/scale),file=outFile)

                        print("    </coordinates>",file=outFile)
                        print("   </LineString>",file=outFile)
                        print("  </Placemark>",file=outFile)

                        # Draw sigmas
                        if (results.eon == True):
                            print("  <Placemark>",file=outFile)
                            print("   <Style>",file=outFile)
                            print("    <LineStyle>",file=outFile)
                            print("     <color>FF000000</color>",file=outFile)
                            print("     <width>2</width>",file=outFile)
                            print("    </LineStyle>",file=outFile)
                            print("    <PolyStyle>",file=outFile)
                            print("     <color>FF000000</color>",file=outFile)
                            print("     <fill>0</fill>",file=outFile)
                            print("    </PolyStyle>",file=outFile)
                            print("   </Style>",file=outFile)
                            print("   <Polygon>",file=outFile)
                            print("    <outerBoundaryIs>",file=outFile)
                            print("     <LinearRing>",file=outFile)
                            print("      <coordinates>",file=outFile)

                            slon = math.sqrt(slon)
                            slat = math.sqrt(slat)
                            srad = math.sqrt(srad)
                            theta = 0

                            if (results.vertical == True):
                                for k in range(0,16):
                                    angle = k/15*2*math.pi
                                    elon = srad*math.cos(angle)*math.cos(theta)-srad*math.sin(angle)*math.sin(theta)
                                    elat = srad*math.cos(angle)*math.sin(theta)+srad*math.sin(angle)*math.cos(theta)
                                    elon = (elon+0)/scale
                                    elat = (elat+vrad)/scale
                                    print("      {:f},{:f},0".format(lon+elon,lat+elat),file=outFile)
                            else:
                                for k in range(0,16):
                                    angle = k/15*2*math.pi
                                    elon = slon*math.cos(angle)*math.cos(theta)-slat*math.sin(angle)*math.sin(theta)
                                    elat = slon*math.cos(angle)*math.sin(theta)+slat*math.sin(angle)*math.cos(theta)
                                    elon = (elon+vlon)/scale
                                    elat = (elat+vlat)/scale
                                    print("      {:f},{:f},0".format(lon+elon,lat+elat),file=outFile)

                            print("      </coordinates>",file=outFile)
                            print("     </LinearRing>",file=outFile)
                            print("    </outerBoundaryIs>",file=outFile)
                            print("   </Polygon>",file=outFile)
                            print("  </Placemark>",file=outFile)

                        # Make table
                        print("{:s} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f} {:12f}".format(
                        test[0],lon,lat,vlon,vlat,vrad,slon,slat,srad),file=txtFile)

    # Finish kml file
    print(" </Folder>",file=outFile)
    print("</kml>",file=outFile)
    outFile.close()
    txtFile.close()

if __name__ == '__main__':
    main()
