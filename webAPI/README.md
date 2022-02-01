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

getDiff  
paras: sta1 sta1 az(optional)   
sample call:
http://172.16.104.138:5000/gpsservice/kml?function=getDiff&sta1=P493&sta2=P503&az=100   
output:   
{"urls": ["http://172.16.104.138:5000/static/kml116420190109140151/P493-P503_az100.txt"], "folder": "kml116420190109140151", "urlprefix": "http://172.16.104.138:5000/static/", "results": ["P493-P503_az100.txt"]}  


Add a new non-required parameter:   
  -- add para to nonrequired list   
  -- set the default value

### interpolation

```
http://localhost:5500/gpsservice/kml?function=getinterpolation&lat=32.97180377635759&lon=-115.55419921875001&width=1.4503504753021161&height=1.0691460280633294&epoch=&epoch1=2010-04-01&epoch2=2011-04-01&scale=&ref=&ct=&pt=&dwin1=&dwin2=&prefix=&mon=false&eon=&vabs=&analysisCenter=
```
The output:
>```{"urlprefix": "http://156.56.174.162:8000/static/", "folder": "kml227020224201144200", "results": ["contour_of_Delta_E.png", "contour_of_Delta_E_colorbar.png", "contour_of_Delta_V.png", "contour_of_LOS_Displacement_colorbar.png", "contour_of_Delta_N_colorbar.png", "displacement_table.txt", "contour_of_Delta_V_colorbar.png", "gps_interpolation.zip", "displacement_horizontal.kml", "contour_of_LOS_Displacement.png", "contour_of_Delta_N.png", "displacement_vertical.kml"], "urls": ["http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_E.png", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_E_colorbar.png", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_V.png", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_LOS_Displacement_colorbar.png", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_N_colorbar.png", "http://156.56.174.162:8000/static/kml227020224201144200/displacement_table.txt", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_V_colorbar.png", "http://156.56.174.162:8000/static/kml227020224201144200/gps_interpolation.zip", "http://156.56.174.162:8000/static/kml227020224201144200/displacement_horizontal.kml", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_LOS_Displacement.png", "http://156.56.174.162:8000/static/kml227020224201144200/contour_of_Delta_N.png", "http://156.56.174.162:8000/static/kml227020224201144200/displacement_vertical.kml"], "imagebounds": [[32.616527, -116.183077], [33.423873, -115.031805]]}```
