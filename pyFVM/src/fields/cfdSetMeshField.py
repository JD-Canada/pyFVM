
def cfdSetMeshField(Region, theMeshField):

    """Adds the input field data (i.e., theMeshField) as a Region.fluid subdict.
    
    """
    
    Region.fluid[theMeshField['name']] = theMeshField