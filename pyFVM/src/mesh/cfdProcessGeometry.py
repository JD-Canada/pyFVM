import numpy as np


def cfdProcessGeometry(mesh):
    """This function processes the mesh geometry"""

#    mesh['faceCentroids']= [[] for i in range(mesh['numberOfFaces'])]
#    mesh['faceSf']= [[] for i in range(mesh['numberOfFaces'])]
#    mesh['faceAreas']= [[] for i in range(mesh['numberOfFaces'])]
    
    mesh['faceWeights']= [[0] for i in range(mesh['numberOfFaces'])]
    mesh['faceCF']= [[0, 0, 0] for i in range(mesh['numberOfFaces'])]
    mesh['faceCf']= [[0,0,0] for i in range(mesh['numberOfFaces'])]
    mesh['faceFf']= [[0,0,0] for i in range(mesh['numberOfFaces'])]
    mesh['wallDist']= [[] for i in range(mesh['numberOfFaces'])]
    mesh['wallDistLimited']= [[] for i in range(mesh['numberOfFaces'])]
    
    mesh['elementCentroids']= [[] for i in range(mesh['numberOfElements'])]
    mesh['elementVolumes']= [[] for i in range(mesh['numberOfElements'])]
    
    
    
    """
    Calculate:
        -face centroids (faceCentroids)
        -face normal (Sf)
        -face areas (faceAreas)
    """
    
    #find cell with largest number of points
    maxPoints=len(max(mesh['faceNodes'], key=len))
    forCross1 = [[] for i in range(maxPoints)]
    forCross2 = [[] for i in range(maxPoints)]
    local_faceCentroid=[[] for i in range(maxPoints)]
    
    for iFace in range(mesh['numberOfFaces']):
        theNodeIndices = mesh['faceNodes'][iFace]
        theNumberOfFaceNodes = len(theNodeIndices)
        
        #compute a rough centre of the face
        local_centre = [0,0,0]
        
        for iNode in theNodeIndices:
            local_centre = local_centre + mesh['nodeCentroids'][int(iNode)]
    
        local_centre = local_centre/theNumberOfFaceNodes
    
        for iTriangle in range(theNumberOfFaceNodes):
            
            point1 = local_centre
            point2 = mesh['nodeCentroids'][int(theNodeIndices[iTriangle])]
            
            if iTriangle < theNumberOfFaceNodes-1:
                point3 = mesh['nodeCentroids'][int(theNodeIndices[iTriangle+1])]
            else:
                point3 = mesh['nodeCentroids'][int(theNodeIndices[0])]
            
            local_faceCentroid[iTriangle].append((point1+point2+point3)/3)
            
            left=point2-point1
            right=point3-point1
            
            forCross1[iTriangle].append(left)
            forCross2[iTriangle].append(right)
        
    
    local_Sf=[np.zeros([mesh['numberOfFaces'],3]) for i in range(maxPoints)]
    local_area=[np.zeros([mesh['numberOfFaces'],3]) for i in range(maxPoints)]
    
    centroid=np.zeros([mesh['numberOfFaces'],3])
    area=np.zeros([mesh['numberOfFaces']])
    Sf=np.zeros([mesh['numberOfFaces'],3])
    
    #cells with fewer faces than others are full of zeros
    for i in range(maxPoints):
        
        forCrossLeft=np.vstack(np.array(forCross1[i]))
        forCrossRight=np.vstack(np.array(forCross2[i]))
        
        local_Sf[i]=0.5*np.cross(forCrossLeft,forCrossRight)
        local_area[i]=np.linalg.norm(local_Sf[i],axis=1)
    
        centroid = centroid + np.array(local_faceCentroid[i])*local_area[i][:,None]
        Sf=Sf+local_Sf[i]
        area=area+local_area[i]
        
    mesh['faceCentroids']=centroid/area[:,None]
    mesh['faceSf']=Sf
    mesh['faceAreas']=area   
    
    
    """
    Pure python version - causes slowness due to iterative np.cross()
    """
    
#    for iFace in range(mesh['numberOfFaces']):
#        theNodeIndices = mesh['faceNodes'][iFace]
#        theNumberOfFaceNodes = len(theNodeIndices)
#        
#        #compute a rough centre of the face
#        local_centre = [0,0,0]
#        
#        for iNode in theNodeIndices:
#            
#            local_centre = local_centre + mesh['nodeCentroids'][int(iNode)]
#    
#        local_centre = local_centre/theNumberOfFaceNodes
#        centroid = [0, 0, 0]
#        Sf = [0,0,0]
#        area = 0
#        
#        #finds area of virtual triangles and adds them to the find to find face area
#        #and direction (Sf)
#    
#                
#        
#        for iTriangle in range(theNumberOfFaceNodes):
#            point1 = local_centre
#            point2 = mesh['nodeCentroids'][int(theNodeIndices[iTriangle])]
#            
#            if iTriangle < theNumberOfFaceNodes-1:
#                point3 = mesh['nodeCentroids'][int(theNodeIndices[iTriangle+1])]
#            else:
#                point3 = mesh['nodeCentroids'][int(theNodeIndices[0])]
#                
#            local_centroid = (point1 + point2 + point3)/3
#            
#            left=point2-point1
#            right=point3-point1
#            x = 0.5*((left[1] * right[2]) - (left[2] * right[1]))
#            y = 0.5*((left[2] * right[0]) - (left[0] * right[2]))
#            z = 0.5*((left[0] * right[1]) - (left[1] * right[0]))
#            local_Sf=np.array([x,y,z])
#    
#            local_area = np.linalg.norm(local_Sf)
#            
#            centroid = centroid + local_area*local_centroid
#            Sf = Sf + local_Sf
#            area = area + local_area
#        centroid = centroid/area
#        mesh['faceCentroids'][iFace]=centroid
#        mesh['faceSf'][iFace]=Sf
#        mesh['faceAreas'][iFace]=area
    
    
    """
    Calculate:
        -element centroids (elementCentroids)
        -element volumes (elementVolumes)
    """
    for iElement in range(mesh['numberOfElements']):
        
        theElementFaces = mesh['elementFaces'][iElement]
        
        #compute a rough centre of the element
        local_centre = [0,0,0]
        
        for iFace in range(len(theElementFaces)):
            faceIndex = theElementFaces[iFace]
            local_centre = local_centre + mesh['faceCentroids'][faceIndex]
        
        local_centre = local_centre/len(theElementFaces)
        
        
        localVolumeCentroidSum = [0,0,0]
        localVolumeSum = 0
        
        for iFace in range(len(theElementFaces)):
            faceIndex = theElementFaces[iFace]
            
            Cf = mesh['faceCentroids'][faceIndex]-local_centre
            
            faceSign = -1
            if iElement == mesh['owners'][faceIndex]:
                faceSign = 1
                
            local_Sf = faceSign*mesh['faceSf'][faceIndex]
            
            localVolume = np.dot(local_Sf,Cf)/3
            
            localCentroid = 0.75*mesh['faceCentroids'][faceIndex]+0.25*local_centre
            
            localVolumeCentroidSum = localVolumeCentroidSum + localCentroid*localVolume
            
            localVolumeSum = localVolumeSum + localVolume
            
        mesh['elementCentroids'][iElement]=localVolumeCentroidSum/localVolumeSum
        mesh['elementVolumes'][iElement]=localVolumeSum
    
    
    for iFace in range(mesh['numberOfInteriorFaces']):
        
        n=mesh['faceSf'][iFace]/np.linalg.norm(mesh['faceSf'][iFace])
        own=mesh['owners'][iFace]
        nei = mesh['neighbours'][iFace]
        
        mesh['faceCF'][iFace]=mesh['elementCentroids'][nei]-mesh['elementCentroids'][own]
        mesh['faceCf'][iFace]=mesh['faceCentroids'][iFace]-mesh['elementCentroids'][own]
        mesh['faceFf'][iFace]=mesh['faceCentroids'][iFace]-mesh['elementCentroids'][nei]
        mesh['faceWeights'][iFace]=(-np.dot(mesh['faceFf'][iFace],n))/(-np.dot(mesh['faceFf'][iFace],n)+np.dot(mesh['faceCf'][iFace],n))
            
        
    for iBFace in range(mesh['numberOfInteriorFaces'], mesh['numberOfFaces']):
        
        
        n=mesh['faceSf'][iBFace]/np.linalg.norm(mesh['faceSf'][iBFace])
        own=mesh['owners'][iBFace]
    
        mesh['faceCF'][iBFace]=mesh['faceCentroids'][iBFace]-mesh['elementCentroids'][own]
        mesh['faceCf'][iBFace]=mesh['faceCentroids'][iBFace]-mesh['elementCentroids'][own]  
        mesh['faceWeights'][iBFace]=1
        mesh['wallDist'][iBFace]= max(np.dot(mesh['faceCf'][iBFace], n), 1e-24)
        mesh['wallDistLimited'][iBFace]= max(mesh['wallDist'][iBFace], 0.05*np.linalg.norm(mesh['faceCf'][iBFace]))