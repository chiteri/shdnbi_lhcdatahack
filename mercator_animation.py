from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.

m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                    llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

nimages = 2
for i in range(0,nimages):

    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    m.fillcontinents(color='black',lake_color='aqua')
    # draw parallels and meridians.
    #m.drawparallels(np.arange(-90.,91.,30.))
    #m.drawmeridians(np.arange(-180.,181.,60.))
    #m.drawmapboundary(fill_color='aqua') 
    m.drawmapboundary(fill_color='black')
    m.drawcoastlines(color='white',linewidth=1) 
    m.drawcountries(color='white') 

    ############################################################################
    # Coordinates for CERN.
    ############################################################################
    lon, lat = 6.1, 46.30
    xpt,ypt = m(lon,lat)
    cern = m.plot(xpt,ypt,'o',color='red',markersize=10)

    # Direction of the beam, along the z axis
    z_direction = 280.2 # degrees as measured from north. So this
                        # is almost due west.
    xpt1 = xpt + 3000000*math.cos(np.deg2rad(z_direction-90))
    ypt1 = ypt + 3000000*math.sin(np.deg2rad(z_direction-90))

    cernz = m.plot([xpt,xpt1],[ypt,ypt1],'-',color='pink',linewidth=4)

    print xpt
    print ypt

    ############################################################################

    #lon = np.linspace(-180,180,10) + i*1
    #lat = np.linspace(-80,80,10) + i*1
    lon = np.linspace(-180,-180+i*2,i+1)
    lat = np.linspace(-80,-80+i*2,i+1)

    print lon
    print lat

    xpt,ypt = m(lon,lat)
    #p = m.plot(xpt,ypt,'o',color='r',markersize=5)
    p = m.plot(xpt,ypt,'-',color='r',linewidth=5)

    plt.title("Mercator Projection")
    name = "merc_with_data_%04d.png" % (i)
    #name = "merc_with_data_%04d.jpg" % (i)
    plt.savefig(name)

    #plt.show()
    plt.clf()

