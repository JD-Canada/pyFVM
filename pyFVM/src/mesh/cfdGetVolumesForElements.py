def cfdGetVolumesForElements(Region):
    
    """Returns the list of element Volumes
    
    
    Attributes:
    
       Region (str): the cfd Region.
       
    Example usage:
    
    cfdGetVolumesForElements(Region)
    
    TODO:
       
       . 
    """
    elementVolumes = Region.mesh['elementVolumes']

    return elementVolumes
