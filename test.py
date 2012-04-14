from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.

#'''
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                    llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
#'''
#m = Basemap(projection='mbtfpq',lon_0=0,resolution='c')

nimages = 50 # This is the number of images (frames) per each 
             # proton collision (dimuon event).

# Open the first file and read its content
nframes_generated = 0
with open('small_muon_sample.dat', 'r' ) as file:

    particle_details = []

    nparticles_read_in = 0 # Use this for a counter for the particles

    for line in file: # Read the data obtained line by line 

        values = line.split()
        print values

        if len(values)==1: # This will tell us how many particles follow.
            del particle_details[:] # Make sure we empty the list each time we
                                    # start a new event.
            no_of_particles = int(values[0])  

        else:
            if nparticles_read_in<no_of_particles:
                particle_details.append(line.split()) # Split the components assuming they are separated by three spaces
                nparticles_read_in += 1
                if nparticles_read_in==no_of_particles: # This means we have read in all the particles.
                    nparticles_read_in = 0 # reset n and start making the images!

                    # I'm going to be lazy here and use an array with two elements,
                    # because we know we are working with events with only two muons.
                    charge = [0.0, 0.0] # charge of the muons.
                    px = [0.0,0.0] # x-component of two muons.
                    pz = [0.0,0.0] # z-component of two muons.

                    # Loop through the number of particles detected in the decay
                    for n in range(0, no_of_particles): 
                         # Convert the next set of inputs into a list 
                         energy, x, y, z, q = particle_details[n] # Unpack the list 
                         px[n] = float(x)
                         pz[n] = float(z)
                         charge[n] = int(q)
                         print energy, x, y, z, q
                         
                    #exit()

                    print px
                    print pz

                    for i in range(0,nimages):

                        #print "frame %d" % (i)

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
                        # Let's make some moving particles.
                        ############################################################################

                       # print data_list
                        for x,y,q in zip(px,pz,charge):

                            velocity_scaling = 20000.0
                            lat = np.linspace(xcms,xcms+i*x*velocity_scaling,i+1)
                            lon = np.linspace(ycms,ycms+i*y*velocity_scaling,i+1)

                            #print lon
                            #print lat

                            #xpt,ypt = m(lon,lat)
                            m.plot(lat,lon,'-',color='r',linewidth=2)

                            # Color the dot, according to the charge of the muon.
                            muon_color='orange'
                            if q<0:
                                muon_color='blue'
                            m.plot(lat[-1],lon[-1],'o',markersize=5,color=muon_color)


                       # plt.title("Muon flight paths")
                        name = "frames/movie_frames_%04d.png" % (nframes_generated)
                        #name = "merc_with_data_%04d.jpg" % (i)
                        plt.savefig(name)

                        #plt.show()
                        plt.clf()
                        nframes_generated += 1

