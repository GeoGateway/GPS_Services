
"""
GPS_servie.py
"""

import random, os, json

from getCoseismic import getCoseismic
from getPostseismic import getPostseismic
from getDisplacement import getDisplacement
from getVelocities import getVelocities

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
	wkpath = os.path.dirname(os.path.realpath(__file__))

	outputdir = wkpath + os.path.sep + wkdir

	if not os.path.exists(outputdir):
		os.mkdir(outputdir)

	return outputdir


def getURLprefix():
	"""return url prefix for output"""

	urlprefix = "http://"

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

	return json.dumps({"urlprefix":urlprefix,"folder":foldername,"results":kmllist})

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
	getVelocities(paras)
	#test coseismic
	paras.output = "coseismic.kml"
	getCoseismic(paras)
	#test postseismic
	paras.output = "postseismic.kml"
	getPostseismic(paras)
	#test displacement
	paras.output = "displacement.kml"
	getDisplacement(paras)


if __name__ == '__main__':
    main()

