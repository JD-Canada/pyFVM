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



def cfdInterpolateGradientFromElementsToInteriorFaces(region,gradPhi,scheme,theNumberOfComponents):
    
    """ Interpolates the gradient's calculated at the cell centers to the face
    """
    
    theNumberOfElements=region.mesh.numberOfElements
    numberOfInteriorFaces = region.mesh.numberOfInteriorFaces
    numberOfFaces = region.mesh.numberOfFaces
    
    ## owners of elements of faces
    owners_f=region.mesh.interiorFaceOwners
    
    ## neighbour elements of faces
    neighbours_f=region.mesh.interiorFaceNeighbours
    
    ## face weights
    g_f=region.mesh.interiorFaceWeights
    
    ## vector formed between owner (C) and neighbour (f) elements
    CF = region.mesh.interiorFaceCF
    
    ## vector of ones
    ones=np.ones((numberOfInteriorFaces))
    
    ## face gradient matrix
    grad_f= np.zeros((numberOfInteriorFaces, 3,theNumberOfComponents))
    
    if scheme == 'linear' or scheme == 'Gauss linear':

        for i in range(theNumberOfComponents):

            """ 
            Example of what is going one in one of the lines below:
                
            a = ones - g_f                              <--- returns a 1D (:,) array (1 - faceWeight)
            b = gradPhi[self.neighbours_f][:,0,i]       <--- grabs only rows in self.neighbours, in column 0, for component 'i'
            c = g_f*self.gradPhi[self.owners_f][:,0,i]  <--- multiplies faceWeight by owners in column 0, for component 'i'
            
            grad_f[:,0,i] = a*self.b + c                <--- fills (:) column '0' for component 'i' with the result of self.a*self.b + self.c 
            
            In words, what is going is:
                
                gradient of phi at face = (1 - faceWeight for cell)*neighbouring element's gradient + faceWeight*owner element's gradient
                
                If the faceWeight (g_f) of the owner cell is high, then its gradient contributes more to the face's gradient than the neighbour cell.
            
            """
            
            grad_f[:,0,i]=(ones-g_f)*gradPhi[neighbours_f][:,0,i]+\
            g_f*gradPhi[owners_f][:,0,i]
            
            grad_f[:,1,i]=(ones-g_f)*gradPhi[neighbours_f][:,1,i]+\
            g_f*gradPhi[owners_f][:,1,i]
            
            grad_f[:,2,i]=(ones-g_f)*gradPhi[neighbours_f][:,2,i]+\
            g_f*gradPhi[owners_f][:,2,i]
            
            return grad_f
        
    if scheme == 'Gauss linear corrected':
        #not yet implemented, but it will have to be
        pass
    
    if scheme == 'Gauss upwind':
        #not yet implemented, but it will have to be
        pass            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    