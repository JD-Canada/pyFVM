import numpy as np
import sys


def interpolateFromElementsToFaces(region,scheme,field):
    
    theInterpolationScheme=scheme
    
    theNumberOfComponents = region.fluid[field].phi.shape[1]
    theNumberOfElements=region.mesh.numberOfElements
    numberOfInteriorFaces = region.mesh.numberOfInteriorFaces
    numberOfFaces = region.mesh.numberOfFaces
    owners = region.mesh.interiorFaceOwners
    neighbours = region.mesh.interiorFaceNeighbours
    
    #interpolation factor p.160 in Moukalled
    g_f=np.asarray(region.mesh.interiorFaceWeights)
    
    #array of ones for subtraction operation below
    ones=np.ones((numberOfInteriorFaces))
    
    #empty array to hold values of phi at the faces
    phi_f=np.zeros((numberOfFaces,theNumberOfComponents))
    
    if theInterpolationScheme == 'linear':
        
        #interpolate centroid values to faces
        for iComponent in range(theNumberOfComponents):
            phi_f[0:numberOfInteriorFaces,iComponent]=g_f*region.fluid[field].phi[neighbours][:,iComponent]+(ones-g_f)*region.fluid[field].phi[owners][:,iComponent]

    if theInterpolationScheme == 'vanLeerV':
        print("vanLeerV is not yet implemented in interpolateFromElementsToFaces")
        sys.exit()

    if theInterpolationScheme == 'linearUpwind':
        print("linearUpwind is not yet implemented in interpolateFromElementsToFaces")
        sys.exit()
 
    for iComponent in range(theNumberOfComponents):
        phi_f[numberOfInteriorFaces:numberOfFaces,iComponent]=region.fluid[field].phi[theNumberOfElements:numberOfFaces,iComponent]

    return phi_f