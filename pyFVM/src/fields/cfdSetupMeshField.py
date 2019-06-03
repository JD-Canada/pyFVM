from pyFVM.src.fields.cfdSetMeshField import cfdSetMeshField


def cfdSetupMeshField(Region,theName, theType):

    """Create an empty dictionary used to initialize the field.
    
    The created dictionary is later passed to cfdSetMeshField(), where it is
    attached to Region.fluid as a sub-dictionary (e.g. Region.fluid[theMeshField['name']]).
    Detects if field is either type volScalar, volVector, surfaceScalar, or 
    surfaceVector3 and creates an empty container with an adequate number of rows
    and columns (i.e., scalar = 1 column, vector = 3 columns) to hold field data.
    
    Attributes:
        
       Region (class instance): contains simulation's mesh.
       theMeshField (dict): dictionary that will hold data.
       theMeshField['name'] (str): name of field (i.e. theName).
       theMeshField['type'] (str): field type (i.e. theType).
       
    Example usage:
        
        fieldDictionary = cfdSetupMeshField(Region,theName, theType)
        
    TODO:
        Pretty sure this is done.
    """
    
    theMeshField={}
    theMeshField['name'] = theName
    theMeshField['type'] = theType
    
    if theType == 'volScalarField':
        
        theInteriorArraySize = Region.mesh['numberOfElements']
        theBoundaryArraySize = Region.mesh['numberOfBElements']
        theMeshField['phi']= [[0] for i in range(theInteriorArraySize+theBoundaryArraySize)]
        print('volScalarField read')
    
    if theType == 'volVectorField':
        
        theInteriorArraySize = Region.mesh['numberOfElements']
        theBoundaryArraySize = Region.mesh['numberOfBElements']
        theMeshField['phi']= [[0, 0, 0] for i in range(theInteriorArraySize+theBoundaryArraySize)]
        print('volVectorField read')
        
    if theType == 'surfaceScalarField':
        
        theInteriorArraySize = Region.mesh['numberOfInteriorFaces']
        theBoundaryArraySize = Region.mesh['numberOfBFaces']
        theMeshField['phi']= [[0] for i in range(theInteriorArraySize+theBoundaryArraySize)]
        print('surfaceScalarField read')  
        
    if theType == 'surfaceVector3Field':
        
        theInteriorArraySize = Region.mesh['numberOfInteriorFaces']
        theBoundaryArraySize = Region.mesh['numberOfBFaces']
        theMeshField['phi']= [[0,0,0] for i in range(theInteriorArraySize+theBoundaryArraySize)]
        print('surfaceVector3Field read')    
    
    #Previous iteration
    theMeshField['prevIter']={}
    theMeshField['prevIter']['phi']=theMeshField['phi']
    
    #Previous time step
    theMeshField['prevTimeStep']={}
    theMeshField['prevTimeStep']['phi']=theMeshField['phi']
    
    cfdSetMeshField(Region, theMeshField)