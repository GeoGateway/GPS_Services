"""
setLocaldata.py
        -- download the data to local
        -- shall setup as a cron job
"""

from __future__ import print_function

import os
import sys
import urllib.request
import glob


def get_localdata(site):
    """get localdata"""

    series = "localdata/" + site + ".series"
    if os.path.exists(series):
        with open(series, "r") as f:
            data = f.read()
    else:
        location = (
            "https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/"
            + site
            + ".series"
        )
        request = urllib.request.Request(location)
        response2 = urllib.request.urlopen(request)
        data = response2.read().decode("utf-8")
        with open(series, "w") as f:
            f.write(data)

    return data.splitlines()


def get_localdata_NGL(site):
    """get localdata for NGL"""

    series = "localdata/" + site + ".tenv3"
    if os.path.exists(series):
        with open(series, "r") as f:
            data = f.read()
    else:
        location = (
            "https://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/" + site + ".tenv3"
        )
        request = urllib.request.Request(location)
        try:
            response2 = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            return []
        data = response2.read().decode("utf-8")
        with open(series, "w") as f:
            f.write(data)
    # NGL data first line is the header
    return data.splitlines()[1:]


def main():
    if not os.path.exists("localdata"):
        os.mkdir("localdata")

    # Read table of positions
    response1 = urllib.request.urlopen(
        "https://sideshow.jpl.nasa.gov/post/tables/table2.html"
    )
    lines = response1.read().decode("utf-8").splitlines()
    stations = []
    for i in range(0, len(lines)):
        test = lines[i].split()
        # 7ODM POS    34.116408361  -117.093197031      762069.350   0.786   0.645   2.751
        if len(test) == 8:
            stations.append(test[0])
    stations = set(stations)
    # print("Total number of stations: ",len(stations))

    for site in stations:
        site_url = (
            "https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/"
            + site
            + ".series"
        )
        cmd = "wget " + site_url + " -N -P localdata"
        # print("downloading: ",site)
        os.system(cmd)

    # update NFL data
    for entry in glob.glob("localdata/*.tenv3"):
        site = entry.split("/")[1]
        site_url = "https://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/" + site
        cmd = "wget " + site_url + " -N -P localdata"
        os.system(cmd)


if __name__ == "__main__":
    main()
