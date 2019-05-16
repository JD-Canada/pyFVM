
def cfdProcessElementTopology(mesh):
    elementNeighbours = [[] for i in range(0,mesh['numberOfElements'])]
    elementFaces = [[] for i in range(0,mesh['numberOfElements'])]
    
    """
    Each index in elementNeighbours corresponds to an element (cell) in the domain
    The elements that neighbour that cell are contained in that index's associated
    list.

    Along the same lines, elementFaces contains list of the faces owned by each 
    element in the domain.

    Watch out, converting between 1 and 0 based indexing might get tricky
    """

    for iFace in range(mesh['numberOfInteriorFaces']):
        own=mesh['owners'][iFace]
        nei=mesh['neighbours'][iFace]
        
        #adds indices of neighbour cells
        elementNeighbours[own].append(nei)
        elementNeighbours[nei].append(own)
        
        #adds interior faces
        elementFaces[own].append(iFace)
        elementFaces[nei].append(iFace)
    
    #adds boundary faces ('patches')
    for iFace in range(mesh['numberOfInteriorFaces'],mesh['numberOfFaces']):
        own=mesh['owners'][iFace]
        elementFaces[own].append(iFace)
        
    
    elementNodes = [[] for i in range(0,mesh['numberOfElements'])]
    
    for iElement in range(mesh['numberOfElements']):
        
        for faceIndex in elementFaces[iElement]:
            elementNodes[iElement].append(mesh['faceNodes'][faceIndex])
        
        
        elementNodes[iElement] = list(set([item for sublist in elementNodes[iElement] for item in sublist]))
    
    upperAnbCoeffIndex=[[] for i in range(0,mesh['numberOfInteriorFaces'])]
    lowerAnbCoeffIndex=[[] for i in range(0,mesh['numberOfInteriorFaces'])]
    
    for iElement in range(mesh['numberOfElements']):
        iNb=1
        for faceIndex in elementFaces[iElement]:
            
            #skip if it is a boundary face
            if faceIndex > mesh['numberOfInteriorFaces']-1:
                continue
            
            own = mesh['owners'][faceIndex]
            nei = mesh['neighbours'][faceIndex]
            
            if iElement == own:
                upperAnbCoeffIndex[faceIndex] = iNb
            elif iElement == nei:
                lowerAnbCoeffIndex[faceIndex] = iNb
                
            iNb = iNb +1
    
    mesh['elementNeighbours']=elementNeighbours
    mesh['elementFaces']=elementFaces
    mesh['elementNodes']=elementNodes
    mesh['upperAnbCoeffIndex']=upperAnbCoeffIndex
    mesh['lowerAnbCoeffIndex']=lowerAnbCoeffIndex
    
    