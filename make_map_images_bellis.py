from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.

'''
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                    llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
'''
m = Basemap(projection='mbtfpq',lon_0=0,resolution='c')

nimages = 50
for i in range(0,nimages):

    #m.shadedrelief()
    #m.etopo()

    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    m.fillcontinents(color='black',lake_color='aqua')
    m.drawmapboundary(fill_color='black')
    m.drawcoastlines(color='white',linewidth=1) 
    m.drawcountries(color='white') 

    # draw parallels and meridians.
    #m.drawparallels(np.arange(-90.,91.,30.))
    #m.drawmeridians(np.arange(-180.,181.,60.))
    #m.drawmapboundary(fill_color='aqua') 

    ############################################################################
    # Coordinates for CERN.
    ############################################################################
    lon, lat = 6.1, 46.30
    xcms,ycms = m(lon,lat)
    cms_detector = m.plot(xcms,ycms,'o',color='red',markersize=10)

    # Direction of the beam, along the z axis
    z_direction = 280.2 # degrees as measured from north. So this
                        # is almost due west.
    xpt1 = xcms + 3000000*math.cos(np.deg2rad(z_direction-90))
    ypt1 = ycms + 3000000*math.sin(np.deg2rad(z_direction-90))

    cms_detector_z = m.plot([xcms,xpt1],[ycms,ypt1],'-',color='pink',linewidth=2)
    #print xpt
    #print ypt

    ############################################################################
    # Coordinates for Nairobi.
    ############################################################################
    lon, lat = 36.82, 1.28
    xpt,ypt = m(lon,lat)
    nairobi = m.plot(xpt,ypt,'o',color='yellow',markersize=10)

    ############################################################################
    # Let's just make some random moving particles.
    ############################################################################

    px = [2.0,10.0] # x-component of two muons.
    py = [3.0,-8.0] # x-component of two muons.

    for x,y in zip(px,py):

        velocity_scaling = 20000.0
        lat = np.linspace(xcms,xcms+i*x*velocity_scaling,i+1)
        lon = np.linspace(ycms,ycms+i*y*velocity_scaling,i+1)

        print lon
        print lat

        #xpt,ypt = m(lon,lat)
        m.plot(lat,lon,'-',color='r',linewidth=2)
        m.plot(lat[-1],lon[-1],'o',markersize=5,color='cyan')

    plt.title("Muon flight paths")
    name = "frames/movie_frames_%04d.png" % (i)
    #name = "merc_with_data_%04d.jpg" % (i)
    plt.savefig(name)

    #plt.show()
    plt.clf()

