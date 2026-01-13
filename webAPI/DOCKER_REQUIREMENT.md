## Storage requirements for Docker
Two storage volumes:
```
# Use Docker named volumes instead of bind mounts
- gps-static-data:/app/static
- gps-local-data:/app/localdata
# Optionally mount config file
- ./GPSService.ini:/app/GPSService.ini
```
The overall storage is small and 1~2 GB shall be enough.  

### /app/static 
The folder holds the outputs from GPS services.  
/static/kml[a random time stamp]  
The contents of this folder shall be accessible from the web front end.  
Example: /static/kml20260112002121 => https://data.geo-gateway.org/static/kml20260112002121   
The server url is defined in GPSService.ini  
```
urlprefix = https://data.geo-gateway.org/static/
```
**Notice** currently we don't save the outpunts in user spaces, the contents of this folder can be deleted. 

### /app/localdata
The folder saves the downloaded GPS seriese data as a local cache.  
GPS service uses the data in local cache to speed up the computation.  
"setLocaldata.py" updates the local cache,   
**Setup a cronjob** to run setLocaldata.py at least once a week, e.g. the middle night of every Saturday.  
