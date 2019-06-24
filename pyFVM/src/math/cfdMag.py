def cfdMag(valueVector):
    
    """Returns the magnitude of a vector or list of vectors
    
    
    Attributes:
    
       valueVector
       
    Example usage:
    
    cfdGetVolumesForElements(U)
    
    TODO:
       
       . 
    """

    import numpy as np
   
    
    
    try:
        iter(valueVector[0])
        result = []
        for iVector in valueVector:
            dotProduct = np.vdot(iVector,iVector)
            magnitude = np.sqrt(dotProduct)
            result.append(magnitude)
       
    except TypeError:   
        dotProduct = np.vdot(valueVector,valueVector)
        magnitude = np.sqrt(dotProduct)
        result = magnitude
        
    return result
