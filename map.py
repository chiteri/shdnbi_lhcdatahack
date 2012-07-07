from mpl_toolkits.basemap import Basemap
import math 
import numpy as np  

def make_map():
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

    # Fill in the map. 
    m.drawcoastlines()
    m.drawcoastlines() 
    m.fillcontinents(color='black',lake_color='aqua')
    m.drawmapboundary(fill_color='black') 
    m.drawcoastlines(color='white',linewidth=1) 
    m.drawcountries(color='white') 

    ############################################################################
    # Coordinates for CERN. 
    ############################################################################
    lon, lat = 6.1, 46.30
    xcms,ycms = m(lon,lat)
    cms_detector = m.plot(xcms,ycms,'o',color='cyan',markersize=5) 

    # Direction of the beam, along the z axis
    z_direction = 280.2 # degrees as measured from north. So this is almost due West 
    xpt1 = xcms + 3000000*math.cos(np.deg2rad(z_direction-90))
    ypt1 = ycms + 3000000*math.sin(np.deg2rad(z_direction-90))

    cms_detector_z = m.plot([xcms,xpt1],[ycms,ypt1],'<-',color='pink',linewidth=2)

    ############################################################################
    # Coordinates for Nairobi.
    ############################################################################
    lon, lat = 36.82, 1.28
    xpt,ypt = m(lon,lat)

    # Have the markersize change with each frame.


    ############################################################################
    # Coordinates for Nairobi.
    ############################################################################
    lon, lat = 36.82, 1.28
    xpt,ypt = m(lon,lat)

    # Have the markersize change with each frame.
    markersize=4*(np.sin(10*0.1)+1.0)

    # Draw three different markers, to represent the Kenyan flag.
    nairobi = m.plot(xpt,ypt,'o',color='green',markersize=3.0*markersize,marker='s')
    nairobi = m.plot(xpt,ypt,'o',color='red',markersize=2.0*markersize,marker='s')
    nairobi = m.plot(xpt,ypt,'o',color='black',markersize=markersize,marker='s')

    return m 

