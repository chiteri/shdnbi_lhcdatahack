import numpy as np

################################################################################
# Calculate the invariant mass according to the theory of special relativity
################################################################################
def invariant_mass(E,px,py,pz):
    mass  = (E[0]+E[1])**2
    mass -= (px[0]+px[1])**2
    mass -= (py[0]+py[1])**2
    mass -= (pz[0]+pz[1])**2

    return np.sqrt(mass)

def calc_invariant_mass(E, px, py, pz, number_of_events):	
    energies = px_sum = py_sum = pz_sum =  0.00 
    
    for n in range (0, number_of_events ): 
        energies  += E[n]
        px_sum += px[n] 
        py_sum += py[n] 
        pz_sum += pz [n]
        break # Force the program to iterate to the next loop, stop execution temporarily
    
    try:
        return np.sqrt( energies**2 - (px_sum**2 + py_sum**2 + pz_sum**2) ) # Return the root of the value obtained
    except ValueError: 
	return 1.0 # 'Houston, we have a problem!'
