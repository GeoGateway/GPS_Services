# GPS Services FastAPI

FastAPI port of the Flask wrapper in `webAPI/`. Command-line GPS tools are unchanged; this folder only replaces the web framework.

Dependencies are managed with `uv`.

## Local run

```bash
cd fastAPI
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

- `GET /gpsservice/test`
- `GET /gpsservice/kml?function=...`
- Static output files: `http://localhost:8000/static/<folder>/...`

Sample calls:

```bash
curl http://localhost:8000/gpsservice/test

curl 'http://localhost:8000/gpsservice/kml?function=getvelocities&lat=33.1&lon=-115.1&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false'

curl 'http://localhost:8000/gpsservice/kml?function=getDiff&sta1=P493&sta2=P503&az=100'
```

Concurrent smoke test:

```bash
uv run python testAPI.py localhost:8000
```

## Docker

```bash
docker compose up --build -d
curl http://localhost:8000/gpsservice/test
```

The container listens on port `8000`. Update `GPSService.ini` `urlprefix` if the public host or port differs from `http://localhost:8000/static/`.
