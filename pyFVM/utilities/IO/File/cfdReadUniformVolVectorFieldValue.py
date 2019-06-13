
def cfdReadUniformVolVectorFieldValue(volVectorFieldEntry):

    """Returns [u,v,w] type list from a 'value uniform (u v w)' dictionary entry. 
    
    Basically strips off '(' and ')' and returns a python list object, e.g. 
    [0, 1.2, 5]
    
    Attributes:
        
       volVectorFieldEntry (list): list containing ['uniform', '(u', 'v','w)']
       
    Example usage:
        
        Region = cfdReadUniformVolVectorFieldValue(volVectorFieldEntry)
        
    """    
    
    vector=[]
    
    for item in volVectorFieldEntry:
        
        if item == 'uniform':
            uniform='uniform'
            continue
    
        item=item.replace("(","")
        item=item.replace(")","")
        
        vector.append(float(item))
        
    return uniform, vector