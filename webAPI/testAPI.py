from multiprocessing.pool import ThreadPool
from time import time as timer
import requests
import argparse


# test velocities
urls = [
    "function=getvelocities&lat=33.1&lon=-115.1&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getvelocities&lat=33.2&lon=-115.2&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getvelocities&lat=33.3&lon=-115.3&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getvelocities&lat=33.4&lon=-115.4&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    ]

#test displacement
urls = [
    "function=getdisplacement&lat=33.1&lon=-115.1&width=2&height=2&epoch=&epoch1=2010-04-07&epoch2=2010-04-09&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getdisplacement&lat=33.2&lon=-115.2&width=1&height=1&epoch=&epoch1=2010-04-07&epoch2=2010-04-09&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getdisplacement&lat=33.3&lon=-115.3&width=1&height=1&epoch=&epoch1=2010-04-07&epoch2=2010-04-09&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
    "function=getdisplacement&lat=33.4&lon=-115.4&width=1&height=1&epoch=&epoch1=2010-04-07&epoch2=2010-04-09&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false",
]

def fetch_url(url):
    try:
        response = requests.get(url)
        #print(realurl)
        return url, response.text, None
    except Exception as e:
        return url, None, e

def apipool_test(apiservername):
    apiserver = "http://" + apiservername + "/gpsservice/kml?"
    fullurls = [apiserver + x for x in urls]
    print("testing started: " + apiserver)
    start = timer()
    results = ThreadPool(4).imap_unordered(fetch_url, fullurls)
    for url, html, error in results:
        if error is None:
            print("%r fetched in %ss" % (url, timer() - start))
            #print(html)
        else:
            print("error fetching %r: %s" % (url, error))
    print("Total Elapsed Time: %s" % (timer() - start,))

def get_servername():
    """ set up ip/hostname of API server """
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="server name and port number")
    args = parser.parse_args()
    
    return args.server


def main():

    # Read command line arguments
    apiserver = get_servername()
    apipool_test(apiserver)

if __name__ == '__main__':
    main()
