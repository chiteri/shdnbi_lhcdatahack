from mpl_toolkits.basemap import Basemap
import math 
import numpy as np  

# Cordinates to be used by the program 
# Coordinates for CERN and Nairobi 
LONGITUDE = {'CERN':6.1, 'Nairobi':36.82 }
LATITUDE = {'CERN':46.3, 'Nairobi': 1.28}

# Direction of the beam, along the z axis 
Z_DIRECTION = 280.2 # degrees as measured from north. So this is almost due West 

def make_map(frame_no):
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

    # Fill in the map. 
    # m.shadedrelief() 
    # m.etopo()
    m.drawcoastlines()
    m.drawcoastlines() 
    m.fillcontinents(color='black',lake_color='aqua')
    m.drawmapboundary(fill_color='black') 
    m.drawcoastlines(color='white',linewidth=1) 
    m.drawcountries(color='white') 

    ###########################################################################
    # Display CMS somewhere in CERN 
    ##########################################################################
    xcms,ycms = m(LONGITUDE['CERN'], LATITUDE['CERN'])
    cms_detector = m.plot(xcms,ycms,'o',color='cyan',markersize=5) 

    # Direction of the beam, along the z axis
    xpt1 = xcms + 3000000*math.cos(np.deg2rad(Z_DIRECTION-90))
    ypt1 = ycms + 3000000*math.sin(np.deg2rad(Z_DIRECTION-90))

    cms_detector_z = m.plot([xcms,xpt1],[ycms,ypt1],'<-',color='pink',linewidth=2)

    ############################################################################
    # Coordinates for Nairobi.
    ############################################################################
    xpt,ypt = m(LONGITUDE['Nairobi'],LATITUDE['Nairobi'])

    # Have the markersize change with each frame.
    markersize=4*(np.sin(frame_no*0.1)+1.0)

    # Draw three different markers, to represent the Kenyan flag.
    nairobi = m.plot(xpt,ypt,'o',color='green',markersize=3.0*markersize,marker='s')
    nairobi = m.plot(xpt,ypt,'o',color='red',markersize=2.0*markersize,marker='s')
    nairobi = m.plot(xpt,ypt,'o',color='black',markersize=markersize,marker='s')

    return m 

