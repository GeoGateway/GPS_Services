GPS_Servies

A very simple flask wrapper for the functions in GPS_Scripts

functions: [required paras][non-required paras]    
getVelocities:[output,lat,lon,width,height][scale,ref,eon,mon]     
getCoseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,eon,mon]  
getPostseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,pt,eon,mon]    
getDisplacemnet:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon,dwin1,dwin2]
getModel:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon]   

sample call:  
http://192.168.59.130:5000/gpsservice/kml?function=getPostseismic&lat=33&lon=-115&width=2&height=2&epoch=2010-04-08   
output:  
{"folder": "kml1867", "urlprefix": "http://", "results": ["postseismic.txt", "postseismic.kml"]}  


