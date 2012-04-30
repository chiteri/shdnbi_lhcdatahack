from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math

################################################################################
# Calculate the invariant mass according to the theory of special relativity
################################################################################
def invariant_mass(E,px,py,pz):

    #print E,px,py,pz

    mass  = (E[0]+E[1])**2
    mass -= (px[0]+px[1])**2
    mass -= (py[0]+py[1])**2
    mass -= (pz[0]+pz[1])**2

    return np.sqrt(mass)

################################################################################

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

# Set this, in case we don't want to read in all 100k events.
max_nevents = 50 # number of p-p collisions.
nevents = 0

nframes_generated = 0

# Open the first file and read its content
#with open('one_event_muon_sample.dat', 'r' ) as file:
#with open('small_muon_sample.dat', 'r' ) as file:
with open('Resources/data_2_muons.dat','r') as file: # This is the big file

    particle_details = []

    nparticles_read_in = 0 # Use this for a counter for the particles

    for line in file: # Read the data obtained line by line 

        if nevents>max_nevents:
            exit(1)

        values = line.split()
        print values

        if len(values)==1: # This will tell us how many particles follow.
            del particle_details[:] # Make sure we empty the list each time we
                                    # start a new event.
            no_of_particles = int(values[0])  
            nevents += 1
            print "nevents: %d" % (nevents)

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
                    py = [0.0,0.0] # y-component of two muons.
                    pz = [0.0,0.0] # z-component of two muons.
                    E = [0.0,0.0] # z-component of two muons.

                    # Loop through the number of particles detected in the decay
                    for n in range(0, no_of_particles): 
                         # Convert the next set of inputs into a list 
                         energy, x, y, z, q = particle_details[n] # Unpack the list 
                         px[n] = float(x)
                         py[n] = float(y)
                         pz[n] = float(z)
                         charge[n] = int(q)
                         E[n] = float(energy)
                         #print energy, x, y, z, q
                         
                    # Now that we have all the particles for a given events,
                    # we generate the frames of the movie.
                    for i in range(0,nimages):

                        # These are cool looking, but they take a lot of time
                        # on the computer to render.
                        #m.shadedrelief()
                        #m.etopo()

                        # Fill in the map.
                        m.drawcoastlines()
                        m.fillcontinents(color='black',lake_color='aqua')
                        m.drawmapboundary(fill_color='black')
                        m.drawcoastlines(color='white',linewidth=1) 
                        m.drawcountries(color='white') 

                        # draw parallels and meridians.
                        #m.drawparallels(np.arange(-90.,91.,30.))
                        #m.drawmeridians(np.arange(-180.,181.,60.))
                        #m.drawmapboundary(fill_color='aqua') # This fills in the oceans.

                        ############################################################################
                        # Coordinates for CERN.
                        ############################################################################
                        lon, lat = 6.1, 46.30
                        xcms,ycms = m(lon,lat)
                        cms_detector = m.plot(xcms,ycms,'o',color='cyan',markersize=5)

                        # Direction of the beam, along the z axis
                        z_direction = 280.2 # degrees as measured from north. So this
                                            # is almost due west.
                        xpt1 = xcms + 3000000*math.cos(np.deg2rad(z_direction-90))
                        ypt1 = ycms + 3000000*math.sin(np.deg2rad(z_direction-90))

                        cms_detector_z = m.plot([xcms,xpt1],[ycms,ypt1],'<-',color='pink',linewidth=2)
                        #print xpt
                        #print ypt

                        ############################################################################
                        # Coordinates for Nairobi.
                        ############################################################################

                        lon, lat = 36.82, 1.28
                        xpt,ypt = m(lon,lat)

                        # Have the markersize change with each frame.
                        markersize=4*(np.sin(nframes_generated*0.1)+1.0)

                        # Draw three different markers, to represent the Kenyan flag.
                        nairobi = m.plot(xpt,ypt,'o',color='green',markersize=3.0*markersize,marker='s')
                        nairobi = m.plot(xpt,ypt,'o',color='red',markersize=2.0*markersize,marker='s')
                        nairobi = m.plot(xpt,ypt,'o',color='black',markersize=markersize,marker='s')

                        ############################################################################
                        # Let's make some moving particles.
                        ############################################################################

                        # Calculate the mass of the theoretical particle that could have decayed
                        # to the two muons. 
                        mass_of_parent_particle = invariant_mass(E,px,py,pz)

                        for x,z,q,energy in zip(px,pz,charge,E):

                            velocity_scaling = 200000.0

                            # To make them move at the same velocity, we only worry about the direction,
                            # and not the scale.
                            angle = np.arctan2(z,x) # use this to get the proper angle.
                            distance_moved = i*velocity_scaling

                            # Calculate a new x and y, just to move the muons in the image frame.
                            x = distance_moved*np.cos(angle)
                            z = distance_moved*np.sin(angle)

                            lat = np.linspace(xcms,xcms+x,i+1)
                            lon = np.linspace(ycms,ycms+z,i+1)

                            # This is a line to represent the flight path of the muon.
                            linewidth = 1.0
                            color = 'r' # 
                            m.plot(lat,lon,'-',color='r',linewidth=linewidth)

                            # This is a dot to represent the position of the muon.
                            # Color the dot, according to the charge of the muon.
                            muon_color='orange' # + charge muon
                            if q<0:
                                muon_color='blue' # - charge muon

                            # Set the size of the muon to be proportional to its energy.
                            markersize = energy*2.0
                            m.plot(lat[-1],lon[-1],'o',markersize=markersize,color=muon_color)

                        ########################################################
                        # Create a marker at CERN that represents the theoretical particle
                        # that could have created the two muons.
                        ########################################################

                        markersize=mass_of_parent_particle*2.0 # Set the size proportional to the mass.
                        #print mass_of_parent_particle

                        # Have the transparency fade out over the time of the particles flight.
                        alpha = (nimages-(i/2.0))/float(nimages)
                        color = 'gray'
                        if charge[0]>0 and charge[1]>0:
                            color='orange'
                        elif charge[0]<0 and charge[1]<0:
                            color='blue'
                        parent_particle = m.plot(xcms,ycms,'o',color=color,markersize=markersize,alpha=alpha)

                        ########################################################
                        # Set the title of the map for each frame and save 
                        # the image.
                        ########################################################
                        title = "Muon flight paths (%3d p-p collisions)" % (nevents)
                        plt.title(title)
                        name = "frames/movie_frames_%04d.png" % (nframes_generated)
                        plt.savefig(name)

                        #plt.show()
                        plt.clf()
                        nframes_generated += 1

