GPS_Servies

A very simple flask wrapper for the functions in GPS_Scripts

functions: [required paras][non-required paras]    
getVelocities:[output,lat,lon,width,height][scale,ref,eon,mon,vabs]     
getCoseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,eon,mon,vabs]  
getPostseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,pt,eon,mon,vabs]      
getDisplacemnet:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon,dwin1,dwin2,vabs]  
getModel:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon,vabs]    

sample call:  
http://192.168.59.130:5000/gpsservice/kml?function=getPostseismic&lat=33&lon=-115&width=2&height=2&epoch=2010-04-08   
output:  
{"folder": "kml1867", "urlprefix": "http://", "results": ["postseismic.txt", "postseismic.kml"]}  
http://192.168.59.130:5000/gpsservice/kml?function=getvelocities&lat=33&lon=-115&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=WMDG&ct=&pt=&dwin1=&dwin2=&mon=false&eon=false&vabs=true 

Add a new non-required parameter:   
  -- add para to nonrequired list   
  -- set the default value

