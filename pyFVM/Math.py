import numpy as np

def cfdMag(valueVector):

    """Returns the magnitude of a vector or list of vectors
    
    Attributes:
    
       valueVector
       
    """

    try:
        iter(valueVector[0])
        result = []
        for iVector in valueVector:
#            print(iVector)
            dotProduct = np.vdot(iVector,iVector)
            magnitude = np.sqrt(dotProduct)
           
            result.append(magnitude)

    except TypeError:   
        dotProduct = np.vdot(valueVector,valueVector)
        magnitude = np.sqrt(dotProduct)
        result = magnitude

    return result

def cfdUnit(vector):
    
    return vector/np.linalg.norm(vector,axis=1)[:,None]