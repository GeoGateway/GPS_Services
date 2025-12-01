# GPS Service - Docker Setup

This document describes how to run the GPS Service Flask application using Docker with Miniconda and Python 3.9.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

## Quick Start

### 1. Build the Docker Image

```bash
# Make the build script executable
chmod +x docker-build.sh

# Build the image
./docker-build.sh

# Or build manually
docker build -t gps-service:latest .
```

### 2. Start the Service

```bash
# Make the run script executable
chmod +x docker-run.sh

# Start the service
./docker-run.sh

# Or start manually
docker-compose up -d
```

### 3. Access the Service

Test that the service is running:
```bash
curl http://localhost:5000/gpsservice/test
```

Or open in your browser:
```
http://localhost:5000/gpsservice/test
```

## Docker Commands

### Start the service
```bash
docker-compose up -d
```

### Stop the service
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Restart the service
```bash
docker-compose restart
```

### Rebuild after code changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Docker Volumes

The application uses Docker named volumes to persist data:

### Volume Information
- **gps-static-data**: Stores generated KML files and outputs
- **gps-local-data**: Stores local data files

Volumes are stored in: `/var/lib/docker/volumes/`

### Inspect Volumes
```bash
# View volume details
./docker-volume-inspect.sh

# List volumes
docker volume ls | grep gps

# Inspect specific volume
docker volume inspect webapi_gps-static-data
```

### Access Volume Data
```bash
# List files in static volume
sudo ls -lh /var/lib/docker/volumes/webapi_gps-static-data/_data

# Access from container
docker exec gps-service-api ls -la /app/static
```

### Backup Volumes
```bash
# Backup static data
docker run --rm \
  -v webapi_gps-static-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/static-backup.tar.gz -C /data .

# Backup local data
docker run --rm \
  -v webapi_gps-local-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/localdata-backup.tar.gz -C /data .
```

### Restore Volumes
```bash
# Restore static data
docker run --rm \
  -v webapi_gps-static-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/static-backup.tar.gz -C /data

# Restore local data
docker run --rm \
  -v webapi_gps-local-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/localdata-backup.tar.gz -C /data
```

### Remove Volumes
```bash
# Warning: This will delete all data!
docker-compose down -v

# Or remove specific volume
docker volume rm webapi_gps-static-data
```

## Configuration

### Port Mapping
By default, the service runs on port 5000. To change the port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Maps host port 8080 to container port 5000
```

### Environment Variables
Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` to customize your configuration.

### Volumes
The following directories are mounted as volumes:
- `./static` - For generated KML files and results
- `./localdata` - For local data storage
- `./GPSService.ini` - Configuration file

## Development

### Running in Debug Mode
To run in debug mode, edit `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=development
  - FLASK_DEBUG=1
```

Then restart:
```bash
docker-compose restart
```

### Accessing the Container Shell
```bash
docker exec -it gps-service-api bash
```

### Testing Inside Container
```bash
docker exec -it gps-service-api conda run -n base python -c "import flask; print(flask.__version__)"
```

## Troubleshooting

### Container won't start
Check logs:
```bash
docker-compose logs
```

### Port already in use
Change the port in `docker-compose.yml` or stop the conflicting service.

### Permission issues with volumes
Ensure the `static` and `localdata` directories exist and have proper permissions:
```bash
mkdir -p static localdata
chmod 755 static localdata
```

### Conda environment not activating
Check that the environment name in `environment.yml` matches the one used in the Dockerfile.

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (Gunicorn or uWSGI):
   - Update Dockerfile CMD to use Gunicorn
   - Example: `CMD ["conda", "run", "-n", "base", "gunicorn", "-b", "0.0.0.0:5000", "GPS_service_API:app"]`

2. **Add nginx as reverse proxy**:
   - Add nginx service to `docker-compose.yml`
   - Configure SSL/TLS certificates

3. **Set resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
   ```

4. **Use environment-specific configs**:
   - Create separate `docker-compose.prod.yml`
   - Use: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

## Sample API Calls

### Test Service
```bash
curl http://localhost:5000/gpsservice/test
```

### Get Velocities
```bash
curl "http://localhost:5000/gpsservice/kml?function=getvelocities&lat=33.1&lon=-115.1&width=2&height=2&output=&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false"
```

### Get Diff
```bash
curl "http://localhost:5000/gpsservice/kml?function=getDiff&sta1=P493&sta2=P503&az=100"
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Conda Documentation](https://docs.conda.io/)
