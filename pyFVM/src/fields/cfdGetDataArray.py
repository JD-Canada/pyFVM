def cfdGetDataArray(Region,field):

    """Gets the phi values for Region.fields.field and returns a list of float elements


    Attributes:
        
       Region (str): the cfd Region.
       field (str): the field in Region.fluid
       
    Example usage:
        
        cfdGetDataArray(Region,'rho')
        
    TODO:
       Missing treatment for volVectorFields
       . 
    """      
    phiArray=[]


    if Region.fluid[field]['type']=='surfaceScalarField':
        phi = Region.fluid[field]['phi']
        for iValue in phi:
            phiArray.append(iValue[0])
    
    elif Region.fluid[field]['type']=='volScalarField':
        phi = Region.fluid[field]['phi']
        for iValue in phi:
            phiArray.append(iValue[0])

    
    elif Region.fluid[field]['type']=='volVectorField':
        phi = Region.fluid[field]['phi']
 
    
    
    return phiArray

