import matplotlib.pyplot as plt
import mapping as map 
from physics import calc_invariant_mass as civ
import numpy as np 
import pylab 
# import argparse 

# Constants to be used in the program 
NO_OF_IMAGES = 50 
MAXIMUM_EVENTS = 50 
NO_OF_EVENTS = 0 
GENERATED_FRAMES = 0
VELOCITY_SCALING = 200000.0 

def plot_data(input_file): 	 
    # Format the headings for the data before display 
    # Open the first file and read its content    
    with open(input_file, 'r' ) as file: 		
        for particle_details in file: # Read the data obtained line by line 
            values = particle_details.split() # The first item can tell us if we are looking at daughter particles or four momentum values  
			
            # Four momentum information for an event. Use lists with lengths equal to the number of daughter particles 
            energy = [0.00]*len( values[0] ) # An empty list to hold the values of e
            x_coord = [0.00]*len( values[0] ) # An empty list to hold the values of px
            y_coord = [0.00]*len( values[0] ) # An empty list to hold the values of py
            z_coord = [0.00]*len( values[0] ) # An empty list to hold the values of pz
            charge = [0.0]*len( values[0] ) # An empty list to hold the values of q
			
            invariant_mass = 0.00 # The invariant mass for each parent particle  
            # daughter_particles = 0 
			
            if len( values[0] ) == 1: # We expect single digit (1, 2 ... 9, 2 mostly) daughter particles from decays 
                daughter_particles = int(values[0]) # The first line represents the number of particles to expect in subsequent events for the decay
 
            elif len( values[0] ) > 1: 
                for n in range (0, daughter_particles): 
                    # Get the four momentum data from the list 
                    energy[n], x_coord[n], y_coord[n], z_coord[n], charge[n] = float(values[0]), float(values[1]), float(values[2]), float(values[3]),  int(values[4])  			
                    break # Temporarily stop execution, force the program to go to the next outer loop iteration 
	
                invariant_mass = civ( energy, x_coord, y_coord, z_coord, daughter_particles ) 					
                print repr(invariant_mass).rjust(20),'invariant mass' 

            # We now have all the information for a particular event 
	    for frame in range(0, NO_OF_IMAGES):
	    #  Show the background of the plot as a map  
	    # background = map.make_map()
			
	        for x, z, q, e in zip(x_coord, z_coord, charge, energy):
				
	            #  Show the background of the plot as a map  
		    background = map.make_map()

		    print x, z, q, e
			   
		    angle = np.arctan2(z,x) # Get the proper angle of the particle's movement
		    distance_moved = frame * VELOCITY_SCALING 

		    # Calculate the new z and x just to move the muons in the image frame 
		    x = distance_moved * np.cos(angle) 
		    z = distance_moved * np.sin(angle)

		    xcms, ycms = background(map.LATITUDE['CERN'], map.LONGITUDE['CERN'])

		    # Convert the x and z cordinates to corresponding longitude and latitude values 
		    latitude = np.linspace(xcms, xcms+x, frame+1)
		    longitude = np.linspace(ycms, ycms+z, frame+1)

		    # This is a line to represent the flight path of the muon 
                    line_width = 1.0 
		    color = 'r'
                           
                    # 
		    background.plot(latitude, longitude, '-', color='r', linewidth=line_width)
                                
		    # Draw a dot to represent the position of the muon 
		    muon_color = 'orange' # A muon with +ve charge is orange in color 
		    if q < 0: 
		        muon_color = 'blue' # -ve charged muon 

		    # Set the size of the muon to be proportional to its energy 
		    marker_size = e * 2.0 

		    background.plot(latitude, longitude, 'o', markersize=marker_size, color=muon_color)

                    # plt.title('Muons flight path')
		
		    # plt.show()

                
if __name__ == "__main__": 
    # parser = argparse.ArgumentParser(description='Calculate the invariant mass of parent particles after a decay into muons in a p-p collision.') 
    # parser.add_argument('-f', '--file', type=str, nargs='+', help='The paths to the file(s) holding the input data.') 
	
    # args = parser.parse_args() 
	
    # background = map.make_map() 

    # plot_data (args.file[0])
    plot_data ('resources/small_muon_sample.dat')
                
    # lon, lat = -104.237, 40.125  # Location of the boulder 

    # xpt, ypt = background(lon,lat) 

    # background.plot(xpt,ypt,'bo')

    # plt.plot(lon, lat,'bo')

    #  plt.title('Test map') 
    # plt.show()

