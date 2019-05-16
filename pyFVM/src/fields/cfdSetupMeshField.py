
from pyFVM.src.fields.cfdSetMeshField import cfdSetMeshField


def cfdSetupMeshField(Region,theName, theType):
    
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