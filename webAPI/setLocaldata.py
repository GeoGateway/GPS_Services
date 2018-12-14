"""
	setLocaldata.py
		-- download the data to local
		-- shall setup as a cron job
"""
from __future__ import print_function

import os
import sys
import urllib.request

def main():

    if not os.path.exists('localdata'):
        os.mkdir("localdata")

	# Read table of positions
    response1 = urllib.request.urlopen('https://sideshow.jpl.nasa.gov/post/tables/table2.html')
    lines = response1.read().decode('utf-8').splitlines()
    stations = []
    for i in range(0,len(lines)):
        test = lines[i].split()
	    #7ODM POS    34.116408361  -117.093197031      762069.350   0.786   0.645   2.751
        if (len(test) == 8):
        	stations.append(test[0])
    stations = set(stations)
    print("Total number of stations: ",len(stations))

    for site in stations:
        site_url = 'https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/'+site+'.series'
        cmd = "wget " + site_url + " -P localdata"
        print("downloading: ",site)
        os.system(cmd)

if __name__ == '__main__':
    main()
