
"""
GPS_servie.py
"""

import random, os, json

from getCoseismic import getCoseismic
from getPostseismic import getPostseismic
from getDisplacement import getDisplacement
from getVelocities import getVelocities

from copy import deepcopy

class objdict(dict):

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

def setoutputlocation():
	""" return a folder for output """

	# make a random folder for each job
	wkdir = "kml" + str(random.randint(1,9999)).zfill(4)
	# put output into static folder
	# sample url: http://192.168.59.130:8000/static/kml1867/postseismic.txt

	wkpath = os.path.dirname(os.path.realpath(__file__)) + "/static"

	outputdir = wkpath + os.path.sep + wkdir

	if not os.path.exists(outputdir):
		os.mkdir(outputdir)

	return outputdir


def getURLprefix():
	"""return url prefix for output"""

	import configparser
	config = configparser.ConfigParser()
	config.read('GPSService.ini')

	urlprefix = config['DEFAULT']['urlprefix']

	return urlprefix

def generateKML(args):
	""" main function to generate KMLs """

	#getVelocities:[output,lat,lon,width,height][scale,ref,vertical,eon]
	#getCoseismic:[output,lat,lon,width,height,epoch][scale,ref,vertical,eon,ct]
	#getPostseismic:[output,lat,lon,width,height,epoch][scale,ref,vertical,eon,ct,pt]
	#getDisplacemnet:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,vertical,eon]  
	
	inputdict = {}
	#non-required paras
	nonrequired = ['scale','ref','ct','pt','vertical','eon']
	inputdict['scale'] = None
	inputdict['ref'] = None 
	inputdict['ct'] = None 
	inputdict['pt'] = None
	inputdict['vertical'] = True 
	inputdict['eon'] = True

	for item in nonrequired:
		if item in args:
			inputdict[item] = args[item]

	#pass the required parameters
	required = ['lat','lon','width','height','epoch','epoch1','epoch2']
	for item in required:
		if item in args:
			inputdict[item] = args[item]

	outputdir = setoutputlocation()
	#functions
	calllist = args['function'].split(",")

	for item in calllist:
		if "velocities" in item.lower():
			inputdict['output'] = outputdir + os.path.sep + "velocity.kml"
			paras = objdict(inputdict)
			getVelocities(paras)

		if "coseismic" in item.lower():
			inputdict['output'] = outputdir + os.path.sep + "coseismic.kml"
			paras = objdict(inputdict)
			getCoseismic(paras)

		if "postseismic" in item.lower():
			inputdict['output'] = outputdir + os.path.sep + "postseismic.kml"
			paras = objdict(inputdict)
			getPostseismic(paras)

		if "displacement" in item.lower():
			inputdict['output'] = outputdir + os.path.sep + "displacement.kml"
			paras = objdict(inputdict)
			getDisplacement(paras)

	# list of output file
	kmllist = os.listdir(outputdir)
	urlprefix = getURLprefix()
	foldername = os.path.basename(outputdir)
	urlslist = [urlprefix + foldername + "/" + x for x in kmllist]

	return json.dumps({"urlprefix":urlprefix,"folder":foldername,"results":kmllist,"urls":urlslist})

def main():

	#test funcction call
	#getVelocities.py --lat 33 --lon -115 --width 2 --height 2 -o velocity.kml
	#getPostseismic.py --lat 33 --lon -115 --width 2 --height 2 -o postseismic.kml -t 2010-04-08
	#getCoseismic.py --lat 33 --lon -115 --width 2 --height 2 -o coseismic.kml -t 2010-04-08
	#getDisplacement.py --lat 33 --lon -115 --width 2 --height 2 -t1 2010-04-07 -t2 2010-04-09 -o displacement.kml

	inputdict={}
	inputdict['lat'] = 33
	inputdict['lon'] = -115
	inputdict['width'] = 2
	inputdict['height'] = 2
	inputdict['epoch'] = '2010-04-08'
	inputdict['epoch1'] = '2010-04-07'
	inputdict['epoch2'] = '2010-04-09'
	inputdict['output'] = ''

	#non-required paras
	inputdict['scale'] = None
	inputdict['ref'] = None 
	inputdict['ct'] = None 
	inputdict['pt'] = None
	inputdict['vertical'] = True 
	inputdict['eon'] = True

	paras = objdict(inputdict)
	#test velocities
	paras.output = "velocity.kml"
	print("running velocity...")
	getVelocities(deepcopy(paras))

	#test coseismic
	paras.output = "coseismic.kml"
	print("running coseismic...")
	getCoseismic(deepcopy(paras))
	#test postseismic
	paras.output = "postseismic.kml"
	print("running postseismic...")
	getPostseismic(deepcopy(paras))
	#test displacement
	paras.output = "displacement.kml"
	print("running displacement...")
	getDisplacement(deepcopy(paras))


if __name__ == '__main__':
    main()

