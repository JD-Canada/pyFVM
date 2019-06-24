def cfdGeometricLengthScale(Region):
    
    """Returns the scale of a field in Region. 
    
    
    Attributes:
    
       Region (str): the cfd Region.
       field (str): field of interest
       
    Example usage:
    
    cfdGetFieldScale(Region,'rho')
    
    TODO:
       
       . 
    """
    from pyFVM.src.mesh.cfdGetVolumesForElements import cfdGetVolumesForElements
    
    
    totalVolume = sum(cfdGetVolumesForElements)
    lengthScale = totalVolume ^ (1/3)

    return lengthScale
