import matplotlib.pyplot as plt
import numpy as np 
import pylab
import mapping as map 
from physics import calc_invariant_mass, invariant_mass #  as cim 

# from math import sqrt 
# import argparse 

# Constants to be used in the program 
NO_OF_IMAGES = 50 
MAXIMUM_EVENTS = 50
VELOCITY_SCALING = 200000.0 

def determine_mass(data_file): 	 
    # Format the headings for the data before display 
    # print repr('Energy').ljust(7), repr('X-coord').ljust(7), repr('Y-coord').ljust(7), repr('Z-coord').ljust(7), repr('Charge').ljust(7), repr('Invariant Mass').ljust(20)      
    # print repr('++++++').ljust(7), repr('+++++++').ljust(7), repr('+++++++').ljust(7), repr('+++++++').ljust(7), repr('++++++').ljust(6), repr('++++++++++++++').ljust(20)
    
    total_events = 0 # To keep track of the number of events processed  
    colision = 0 # For each daughter particle in a colision 
    frames_generated = 0 # Count the number of images produced 
    
    energy = [0.00]*2 # An empty list to hold the values of e
    x_coord = [0.00]*2 # An empty list to hold the values of px
    y_coord = [0.00]*2 # An empty list to hold the values of py
    z_coord = [0.00]*2 # An empty list to hold the values of pz
    charge = [0.0]*2 # An empty list to hold the values of q
    
    # Open the first file and read its content    
    with open(data_file, 'r' ) as file: 		
        for particle_details in file: # Read the data obtained line by line 
        
            if total_events > MAXIMUM_EVENTS: 
                exit(1) # Stop execution permanently 
        
            event_data  = particle_details.split() # The first item can tell us if we are looking at daughter particles or four momentum values  
			
            # Four momentum information for an event. Use lists with lengths equal to the number of daughter particles 
            # energy = [0.00]*len( values[0] ) # An empty list to hold the values of e
            # x_coord = [0.00]*len( values[0] ) # An empty list to hold the values of px
            # y_coord = [0.00]*len( values[0] ) # An empty list to hold the values of py
            # z_coord = [0.00]*len( values[0] ) # An empty list to hold the values of pz
            # charge = [0.0]*len( values[0] ) # An empty list to hold the values of q
			
            parent_mass = 0.00 # The invariant mass for each parent particle  
            # daughter_particles = 0 
			
            if len( event_data[0] ) == 1: # We expect single digit (1, 2 ... 9, 2 mostly) daughter particles from decays 
                daughter_particles = int(event_data[0]) # The first line represents the number of particles to expect in subsequent events for the decay
 
            elif len( event_data[0] ) > 1: 
                total_events += 1 # Increment the number 
                if colision < daughter_particles: 
                    # Get the four momentum data from the list 
                    energy[colision], x_coord[colision], y_coord[colision], \
                    z_coord[colision], charge[colision] = float(event_data[0]), \
                    float(event_data[1]), float(event_data[2]), float(event_data[3]),  int(event_data[4])  			
                    # print repr(energy[n]).rjust(8), repr(x_coord[n]).rjust(8), repr(y_coord[n]).rjust(8), repr(z_coord[n]).rjust(8), repr(charge[n]).rjust(8), 
                    # break # Temporarily stop execution, force the program to go to the next outer loop iteration 
                    colision += 1 
                    
                if colision == daughter_particles: 
	
                    # invariant_mass = cim( energy, x_coord, y_coord, z_coord, daughter_particles )
                    parent_mass = invariant_mass ( energy, x_coord, y_coord, z_coord)
                    print repr(parent_mass).rjust(20) 
                    colision = 0 # Reset the counter 
		
                    # The rest of the processing continues using all the information for an event 
                    for frame in range(0, NO_OF_IMAGES):
                        for x, z, q, e in zip(x_coord, z_coord, charge, energy): 
                            print x, z, q, e
                            #  Show the background of the plot as a map  
		            background = map.make_map(frame) 
		        
                            angle = np.arctan2(z,x) # Get the proper angle of the particle's movement 
                            distance_moved = frame * VELOCITY_SCALING 

                            # Calculate the new z and x just to move the muons in the image frame 
                            x = distance_moved * np.cos(angle) 
                            z = distance_moved * np.sin(angle)

                            xcms, ycms = background(map.LONGITUDE['CERN'], map.LATITUDE['CERN'])

                            # Convert the x and z cordinates to corresponding longitude and latitude values 
                            latitude = np.linspace(xcms, xcms+x, frame+1) 
                            longitude = np.linspace(ycms, ycms+z, frame+1)
                        
                            # This is a line to represent the flight path of the muon 
                            line_width = 1.0 
                            colour = 'r'
                           
                            # 
                            background.plot(latitude, longitude, '-', color=colour, linewidth=line_width)
                        
                            # Draw a dot to represent the position of the muon 
                            muon_color = 'orange' # A muon with +ve charge is orange in color 
                        
                            if q < 0: 
                                muon_color = 'blue' # -ve charged muon 

                            # Set the size of the muon to be proportional to its energy 
                            marker_size = e * 2.0 

                            background.plot(latitude[-1], longitude[-1], 'o', markersize=marker_size, color=muon_color)

                            # break 
                        
                        ########################################################
                        # Create a marker at CERN that represents the theoretical particle
                        # that could have created the two muons.
                        ######################################################## 
                        markersize=parent_mass*2.0 # Set the size proportional to the mass.
                    
                        # Have the transparency fade out over the time of the particles flight.
                        alpha = (NO_OF_IMAGES-(frame/2.0))/float(NO_OF_IMAGES)
                        color = 'gray'
                    
                        if charge[0]>0 and charge[1]>0:
                            color='orange'
                        elif charge[0]<0 and charge[1]<0:
                            color='blue'
                        
                        parent_particle = background.plot(xcms,ycms,'o',color=color,markersize=markersize,alpha=alpha) 
                    
                        ########################################################
                        # Set the title of the map for each frame and save 
                        # the image.
                        ########################################################
                        frames_generated += 1 
                        title = "Muons flight paths (%3d p-p colisions)" % (total_events)
                        plt.title(title)
                        image_file = "refactor_frames/movie_frames_%04d.png" % (frames_generated) 
                        
                        # plt.show()
                                        
                        plt.savefig(image_file) 
                        pylab.close(image_file) 
                        plt.clf()
                    
			
if __name__ == "__main__": 
  #  parser = argparse.ArgumentParser(description='Calculate the invariant mass of parent particles after a decay into muons in a p-p collision.') 
   # parser.add_argument('-f', '--file', type=str, nargs='+', help='The paths to the file(s) holding the input data.') 
	
    # args = parser.parse_args() 
	
    determine_mass ('resources/data_2_muons.dat')
