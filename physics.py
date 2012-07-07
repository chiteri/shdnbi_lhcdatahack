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
