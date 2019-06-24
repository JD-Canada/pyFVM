def cfdGetMeshField(Region,field):
    """Returns the field dictionary in Region.fluid['field']. 


    Attributes:
        
       Region (str): the cfd Region.
       field (str): the field in Region.fluid

    Example usage:
        
        rhoField=cfdGetMeshField(Region,'rho')
        
    TODO:
        
        Add fallback
        
       . 
    """    
    
    if field in Region.fluid.keys():
        fieldDict=Region.fluid[field]
        
    else:
        fieldDict=-1
        
    return fieldDict
        
    