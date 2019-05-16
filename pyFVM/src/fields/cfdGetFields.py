


def cfdGetFields(Region):
    """ I am a docstring """
    
    fields=[]
    
    for key in Region.foamDictionary['fvSolution']['solvers']:

        fields.append(key)
        
    return fields
    