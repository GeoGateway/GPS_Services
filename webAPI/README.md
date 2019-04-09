GPS_Servies

A very simple flask wrapper for the functions in GPS_Scripts

functions: [required paras][non-required paras]    
getVelocities:[output,lat,lon,width,height][scale,ref,eon,mon,vabs]     
getCoseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,eon,mon,vabs]  
getPostseismic:[output,lat,lon,width,height,epoch][scale,ref,ct,pt,eon,mon,vabs]      
getDisplacemnet:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon,dwin1,dwin2,vabs]  
getModel:[output,lat,lon,width,height,epoch1,epoch2][scale,ref,eon,mon,vabs]    

sample call:  
http://172.16.104.138:5000/gpsservice/kml?function=getvelocities&lat=33.1&lon=-115.1&width=2&height=2&epoch=&epoch1=&epoch2=&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=false&vabs=false   

output:  
{"results": ["velocity_vertical.kml", "velocity_table.txt", "velocity_horizontal.kml"], "urlprefix": "http://172.16.104.138:5000/static/", "folder": "kml096320193009113018", "urls": ["http://172.16.104.138:5000/static/kml096320193009113018/velocity_vertical.kml", "http://172.16.104.138:5000/static/kml096320193009113018/velocity_table.txt", "http://172.16.104.138:5000/static/kml096320193009113018/velocity_horizontal.kml"]}

Add a new non-required parameter:   
  -- add para to nonrequired list   
  -- set the default value

