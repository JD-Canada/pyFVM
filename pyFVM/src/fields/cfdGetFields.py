


def cfdGetFields(Region):
    
    """Gets field names from keys contained in Region.foamDictionary['fvSolution'].
    
    Attributes:
        
       fields (list): fields.

    Returns:
        
       fields
       
    Example usage:
        
        fields = cfdGetFields(Region)
        
    """
    
    fields=[]
    
    for key in Region.foamDictionary['fvSolution']['solvers']:

        fields.append(key)
        
    return fields
    