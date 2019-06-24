def cfdGetFieldScale(Region,field):
    
    """Returns the scale of a field in Region. 
    
    
    Attributes:
    
       Region (str): the cfd Region.
       field (str): field of interest
       
    Example usage:
    
    cfdGetFieldScale(Region,'rho')
    
    TODO:
       
       . 
    """
    scale = Region.fluid[field].scale
    
    return scale
