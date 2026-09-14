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
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from GPS_service import generateKML
from GPS_service import run_getDiff

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR = BASE_DIR / "templates"
MAP_PAGE = TEMPLATES_DIR / "map.html"

app = FastAPI(title="GPS Services FastAPI")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def index():
    """redirect root to the interactive map interface"""
    return RedirectResponse(url="/map")


@app.get("/map", include_in_schema=False)
@app.get("/gpsservice/map", include_in_schema=False)
def map_page():
    """online interface for the GNSS tools.

    Two-panel split layout: left panel = model selection + parameters
    (mirrors reference/GNSS.vue); right panel = Leaflet map.
    """
    if not MAP_PAGE.exists():
        return Response("map page not found", status_code=404)
    return FileResponse(str(MAP_PAGE), media_type="text/html")


@app.get("/gpsservice/test")
def test():
    info = {}
    info["python"] = sys.version
    info["debug"] = app.debug
    return info


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
