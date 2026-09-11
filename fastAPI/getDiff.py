#!/usr/bin/env python3
# Author:  Developed for GeoGateway by Andrea Donnellan
# Date:  March 19, 2019
# Organization:  JPL, Caltech

from __future__ import print_function

prolog="""
**PROGRAM**
    getDiff.py
      
**PURPOSE**
    Make difference text file from two time sereis

**USAGE**
"""
epilog="""
**EXAMPLE**
    getDiff.py --sta1 P493 --sta2 P503 -o sta1_sta2.txt
               
**COPYRIGHT**
    | Copyright 2019, by the California Institute of Technology
    | United States Government Sponsorship acknowledged
    | All rights reserved

**AUTHORS**
    | Developed for GeoGateway by Andrea Donnellan
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
    parser.add_argument('--sta1', action='store', dest='sta1',required=True,help='station 1')
    parser.add_argument('--sta2', action='store', dest='sta2',required=True,help='station 2')
    parser.add_argument('--az', action='store', dest='az',required=False,help='az')
    return parser

def main():

    # Read command line arguments
    parser = _getParser()
    results = parser.parse_args()
    getDiff(results)

def getDiff(results):
    # Read sta1 sta2 series
    sta1 = results.sta1
    sta2 = results.sta2

    if (results.az):
        output = results.sta1 + "-" + results.sta2 + "_az" + results.az + ".txt"
        angle = 270 - float(results.az)
    else:
        output = results.sta1 + "-" + results.sta2 + ".txt"
        angle = 0.0
    #setup output folder
    output = results.output + output

    #print(angle)
    location1 = 'https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/'+sta1+'.series'
    location2 = 'https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/'+sta2+'.series'

    request1 = urllib.request.Request(location1)
    response1 = urllib.request.urlopen(request1)
    series1 = response1.read().decode('utf-8').splitlines()

    request2 = urllib.request.Request(location2)
    response2 = urllib.request.urlopen(request2)
    series2 = response2.read().decode('utf-8').splitlines()

    outFile = open(output,'w')
    if (results.az):
        print(" date1         dPerp    dPll     dZ       edPerp   edPll    edZ    y1   m1 d1 h1 m1 s1  date2       y2   m2 d2 h2 m2 s2  azimuth = ", results.az ,file=outFile)
    else:
        print(" date1         dE       dN       dV       edE      edN      edV    y1   m1 d1 h1 m1 s1  date2       y2   m2 d2 h2 m2 s2",file=outFile)

    for j in range(0,len(series1)):
        set1 = series1[j].split()
        date1 = float(set1[0])

        for k in range(0,len(series2)):
            set2 = series2[k].split()
            date2 = float(set2[0])
            dd =  date1 - date2
            if(dd < .0027):
                if(dd > -.0027):
                    x = (float(set1[1]) - float(set2[1]))*1000
                    y = (float(set1[2]) - float(set2[2]))*1000
                    z = (float(set1[3]) - float(set2[3]))*1000
                    ex = math.sqrt(float(set1[4])*float(set1[4])+float(set2[4])*float(set2[4]))*1000
                    ey = math.sqrt(float(set1[4])*float(set1[5])+float(set2[5])*float(set2[5]))*1000
                    ez = math.sqrt(float(set1[4])*float(set1[6])+float(set2[6])*float(set2[6]))*1000
                    if (results.az):
                        yp = x*math.cos(math.radians(angle)) + y*math.sin(math.radians(angle))
                        xp = x*math.sin(math.radians(angle)) - y*math.cos(math.radians(angle))
                        eyp = ex*math.cos(math.radians(angle)) - ey*math.sin(math.radians(angle))
                        exp = ex*math.sin(math.radians(angle)) + ey*math.cos(math.radians(angle))
                        print("{:12f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:s} {:>2s} {:>2s} {:>2s} {:>2s} {:>2s} {:12f} {:s} {:>2s} {:>2s} {:>2s} {:>2s} {:>2s}".format(date1,\
xp,yp,z,exp,eyp,ez, set1[11], set1[12], set1[13], set1[14], set1[15], set1[16], \
date2, set2[11], set2[12], set2[13], set2[14], set2[15], set2[16]),file=outFile)
                    else:
                        print("{:12f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f} {:s} {:>2s} {:>2s} {:>2s} {:>2s} {:>2s} {:12f} {:s} {:>2s} {:>2s} {:>2s} {:>2s} {:>2s}".format(date1, x,y,z,ex,ey,ez, set1[11], set1[12], set1[13], set1[14], set1[15], set1[16], date2, set2[11], set2[12], set2[13], set2[14], set2[15], set2[16]),file=outFile)

    outFile.close()


if __name__ == '__main__':
    #testing getDiff1.py  --sta1 P493 --sta2 P503 --az AZIMUTH
    main()

