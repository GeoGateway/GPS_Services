"""
app.py
    FastAPI wrapper for GPS Services command-line tools.

    $ uv sync
    $ uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload

    http://localhost:8000/gpsservice/test
"""

import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from GPS_service import generateKML
from GPS_service import run_getDiff

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="GPS Services FastAPI")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/gpsservice/test")
def test():
    info = {}
    info["python"] = sys.version
    info["runningmode"] = app.debug
    return Response(content=info["python"] + str(info["runningmode"]))


@app.get("/gpsservice/kml")
def kml(request: Request):
    """main function to generate KMLs"""

    args = request.query_params

    try:
        function = args["function"]
    except KeyError:
        return Response("bad request", status_code=400)

    result = ""

    if not function == "getDiff":
        result = generateKML(args)

    if function == "getDiff":
        result = run_getDiff(args)

    return Response(content=result, media_type="application/json")
