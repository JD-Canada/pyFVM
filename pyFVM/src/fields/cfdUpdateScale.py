def cfdUpdateScale(Region,field):

    """Update the min, max and scale values of a field in Region


    Attributes:
        
       Region (str): the cfd Region.
       field (str): the field in Region.fields
       
    Example usage:
        
        cfdUpdateScale(Region,'rho')
        
    TODO:
       
       . 
    """    
        
    from pyFVM.src.fields.cfdGetDataArray import cfdGetDataArray
    from pyFVM.src.fields.cfdGetFieldScale import cfdGetFieldScale
    from pyFVM.src.region.cfdGeometricLengthScale import cfdGeometricLengthScale
    from pyFVM.src.math.cfdMag import cfdMag
    
    
    phi=cfdGetDataArray(Region,field)
    theMagnitude = cfdMag(phi)
    
    try:
        iter(theMagnitude)
        phiMax=max(cfdMag(phi))
        phiMin=min(cfdMag(phi))


    except TypeError:
        phiMax=theMagnitude
        phiMin=theMagnitude
            
    if field=='p':
        vel_scale = cfdGetFieldScale('U')
        rho_scale = cfdGetFieldScale('rho')
        p_dyn = 0.5 * rho_scale * vel_scale^2
        phiScale = max(phiMax,p_dyn)
    
    elif field=='U':
        phiScale = max(cfdGeometricLengthScale,phiMax)
    else: 
        phiScale = phiMax
    
    
    Region.fluid[field]['max']=phiMax
    Region.fluid[field]['min']=phiMin
    Region.fluid[field]['scale']=phiScale


