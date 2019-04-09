"""
    GPS_service_API.py
        -- a minimum flask api wrapper

        $export FLASK_APP=GPS_service.py
        $export FLASK_DEBUG=1
        $python3 -m flask run

        http://localhost:5000/gpsservice/test

"""

import sys
import socket
import json
from flask import Flask
from flask import request
from flask import Response
from GPS_service import generateKML
from GPS_service import run_getDiff

app = Flask(__name__)


"""test service is running"""
@app.route("/gpsservice/test")
def test():
    info={}
    info["python"] = sys.version
    info["runningmode"] = app.debug
    return info["python"] + str(info["runningmode"])


"""generate kml"""
@app.route("/gpsservice/kml")
def kml():
    """ main function to generate KMLs"""
    
    args = request.args

    # assume everything is right
    try:
        function = args['function']
    except KeyError:
        return Response("bad request",status=400)

    result = ""

    if not function == "getDiff":
        result = generateKML(args)

    if function == "getDiff":
        result = run_getDiff(args)

    return result

if __name__ == "__main__":
    pass
    # old method
    #app.run(host='0.0.0.0', debug=False)
