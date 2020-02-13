import numpy as np

import pyFVM.IO as io

class Polymesh():
    """ Handles all mesh related methods.
        
        The Polymesh class takes care of all mesh related operations: 
        Read the polymesh directory and instance the mesh elements (points, faces, neighbours, owners... ) in memory
        Process topology and connectivity
        
    """    
    
    def __init__(self, Region):
        """Sets paths of mesh files, reads in mesh file data and calls numerous functions to process the mesh toplogy.
        """
        
        self.Region=Region
        
        ## Path to points files
        self.pointsFile = r"%s/constant/polyMesh/points" % self.Region.caseDirectoryPath

        ## Path to faces file
        self.facesFile = r"%s/constant/polyMesh/faces" % self.Region.caseDirectoryPath

        ## Path to owner file
        self.ownerFile = r"%s/constant/polyMesh/owner" % self.Region.caseDirectoryPath

        ## Path to neighbour file
        self.neighbourFile = r"%s/constant/polyMesh/neighbour" % self.Region.caseDirectoryPath

        ## Path to boundary file
        self.boundaryFile = r"%s/constant/polyMesh/boundary" % self.Region.caseDirectoryPath 
        
        print('\n')
        print('Reading contents of ./constant/polyMesh folder ...')
        
        self.cfdReadPointsFile()
        self.cfdReadFacesFile()
        self.cfdReadOwnerFile()
        self.cfdReadNeighbourFile()

        #maybe these should go in a function?
        self.numberOfBFaces=self.numberOfFaces-self.numberOfInteriorFaces
        self.numberOfElements = max(self.neighbours)+1 #because of zero indexing in Python
        self.numberOfBElements=self.numberOfFaces-self.numberOfInteriorFaces #seems strange that subtracting faces gives elements ...

        self.cfdReadBoundaryFile()  
        self.cfdCheckIfCavity()
        
        print('Processing mesh ... please wait ....')
        
        self.cfdProcessElementTopology()
        self.cfdProcessNodeTopology()
        self.cfdProcessGeometry()
        
        self.cfdGetBoundaryElementsSubArrayForBoundaryPatch()
        self.cfdGetOwnersSubArrayForBoundaryPatch()
        self.cfdGetFaceSfSubArrayForBoundaryPatch()
        self.cfdGetFaceCentroidsSubArrayForBoundaryPatch()
        
        ## (list) 1D, indices refer to an interior face, list value is the face's owner
        self.interiorFaceOwners = self.owners[0:self.numberOfInteriorFaces]

        ## (list) 1D, indices refer to an interior face, list value is the face's neighbor cell
        self.interiorFaceNeighbours = self.neighbours[0:self.numberOfInteriorFaces]

        ## (list) 1D, face weighting factors. Values near 0.5 mean the face's centroid is approximately halfway between the center of the owner and neighbour cell centers, values less than 0.5 mean the face centroid is closer to the owner and those greater than 0.5 are closer to the neighbour cell).
        self.interiorFaceWeights = self.faceWeights[0:self.numberOfInteriorFaces]

        ## (array) 2D, normal vectors (Sf) of the interior faces (indices refer to face index)
        self.interiorFaceSf = self.faceSf[0:self.numberOfInteriorFaces]
        
        ## (list) 1D, indices refer to an boundary face, list value refers to the face's owner
        self.owners_b = self.owners[self.numberOfInteriorFaces:self.numberOfFaces]

        ## (list) 1D, normal vectors (Sf) of the boundary faces (indices refer to face index). Boundary face normals always point out of the domain. 
        self.Sf_b=self.faceSf[self.numberOfInteriorFaces:self.numberOfFaces]
        
    def cfdReadPointsFile(self):
        """ Reads the constant/polyMesh/points file in polymesh directory and stores the points coordinates
        into region.mesh.nodeCentroids
        """

        with open(self.pointsFile,"r") as fpid:
            
            print('Reading points file ...')
            points_x=[]
            points_y=[]
            points_z=[]
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if len(tline.split()) ==1:
                    if "(" in tline:
                        continue
                    if ")" in tline:
                        continue
                    else:
                        self.numberOfNodes = int(tline.split()[0])
                        continue
                
                tline=tline.replace("(","")
                tline=tline.replace(")","")
                tline=tline.split()
                
                points_x.append(float(tline[0]))
                points_y.append(float(tline[1]))
                points_z.append(float(tline[2]))
        
        ## (array) with the mesh point coordinates 
        self.nodeCentroids = np.array((points_x, points_y, points_z), dtype=float).transpose()


    def cfdReadFacesFile(self):
        """ Reads the constant/polyMesh/faces file and stores the nodes pertaining to each face
            in region.mesh.faceNodes
            Starts with interior faces and then goes through the boundary faces. 
        """ 

        with open(self.facesFile,"r") as fpid:
            print('Reading faces file ...')
            self.faceNodes=[]
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if len(tline.split()) ==1:
                    if "(" in tline:
                        continue
                    if ")" in tline:
                        continue
                    else:
                        
                        self.numberOfFaces = int(tline.split()[0])
                        continue
                
                tline=tline.replace("("," ")
                tline=tline.replace(")","")
                faceNodesi=[]
                for count, node in enumerate(tline.split()):
                    if count == 0:
                        continue
                        #faceNodesi.append(int(node))
                    else:
                        faceNodesi.append(float(node))
                
                self.faceNodes.append(faceNodesi)
                
        ## (array) with the nodes for each face
        self.faceNodes=np.asarray(self.faceNodes)
        print(self.faceNodes)

    def cfdReadOwnerFile(self):
        """ Reads the polyMesh/constant/owner file and returns a list 
        where the indexes are the faces and the corresponding element value is the owner cell
        """ 

        with open(self.ownerFile,"r") as fpid:
            print('Reading owner file ...')

            ## (list) 1D, indices refer to faces, list value is the face's owner cell
            self.owners=[]
            start=False
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
        
                if len(tline.split()) ==1:
                   
                    #load and skip number of owners
                    if not start:
                        nbrOwner=tline
                        start=True
                        continue
        
                    if "(" in tline:
                        continue
                    if ")" in tline:
                        break
                    else:
                        self.owners.append(int(tline.split()[0]))

    def cfdReadNeighbourFile(self):
        """ Reads the polyMesh/constant/neighbour file and returns a list 
        where the indexes are the faces and the corresponding element value is the neighbour cell
        """ 


        with open(self.neighbourFile,"r") as fpid:
            print('Reading neighbour file ...')

            ## (list) 1D, indices refer to faces, list value is the face's owner cell
            self.neighbours=[]
            start=False
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if len(tline.split()) ==1:
                   
                    #load and skip number of owners
                    if not start:
                        self.numberOfInteriorFaces=int(tline)
                        start=True
                        continue
    
                    if "(" in tline:
                        continue
                    if ")" in tline:
                        break
                    else:
                        self.neighbours.append(int(tline.split()[0]))
                       
    
    def cfdReadBoundaryFile(self):
        """Reads the polyMesh/boundary file and reads its contents in a dictionary (self.cfdBoundary)
        """
       
        with open(self.boundaryFile,"r") as fpid:
            print('Reading boundary file ...')
            
            ## (dict) key for each boundary patch
            self.cfdBoundaryPatchesArray={}
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
    
                count=0
                if len(tline.split()) ==1:
                    if "(" in tline:
                        continue
                    if ")" in tline:
                        continue
                    
                    if tline.strip().isdigit():
                        
                        self.numberOfBoundaryPatches = tline.split()[0]
                        continue
                   
                    boundaryName=tline.split()[0]
                    
                    self.cfdBoundaryPatchesArray[boundaryName]=io.cfdReadCfdDictionary(fpid)
                    ## number of faces for the boundary patch
                    self.cfdBoundaryPatchesArray[boundaryName]['numberOfBFaces']= int(self.cfdBoundaryPatchesArray[boundaryName].pop('nFaces'))
                    
                    ## start face index of the boundary patch in the self.faceNodes
                    self.cfdBoundaryPatchesArray[boundaryName]['startFaceIndex']= int(self.cfdBoundaryPatchesArray[boundaryName].pop('startFace'))
                    count=count+1

                    ## index for boundary face, used for reference
                    self.cfdBoundaryPatchesArray[boundaryName]['index']= count
    
                    
    def cfdCheckIfCavity(self):
        
        self.foundPatch=False
        
        for patch, value in self.cfdBoundaryPatchesArray.items():
            
            if value['type'] == 'inlet' or 'outlet':
                self.foundPatch =True
                break


    def cfdProcessElementTopology(self):

        """
        """
        
        self.elementNeighbours = [[] for i in range(0,self.numberOfElements)]
        self.elementFaces = [[] for i in range(0,self.numberOfElements)]
        
    
        for iFace in range(self.numberOfInteriorFaces):
            own=self.owners[iFace]
            nei=self.neighbours[iFace]
            
            #adds indices of neighbour cells
            self.elementNeighbours[own].append(nei)
            self.elementNeighbours[nei].append(own)
            
            #adds interior faces
            self.elementFaces[own].append(iFace)
            self.elementFaces[nei].append(iFace)
        
        #adds boundary faces ('patches')
        for iFace in range(self.numberOfInteriorFaces,self.numberOfFaces):
            own=self.owners[iFace]
            self.elementFaces[own].append(iFace)
            
        
        self.elementNodes = [[] for i in range(0,self.numberOfElements)]
        
        for iElement in range(self.numberOfElements):
            
            for faceIndex in self.elementFaces[iElement]:
                self.elementNodes[iElement].append(self.faceNodes[faceIndex])
            
            
            self.elementNodes[iElement] = list(set([item for sublist in self.elementNodes[iElement] for item in sublist]))
        
        self.upperAnbCoeffIndex=[[] for i in range(0,self.numberOfInteriorFaces)]
        self.lowerAnbCoeffIndex=[[] for i in range(0,self.numberOfInteriorFaces)]
        
        for iElement in range(self.numberOfElements):
            iNb=1
            for faceIndex in self.elementFaces[iElement]:
                
                #skip if it is a boundary face
                if faceIndex > self.numberOfInteriorFaces-1:
                    continue
                
                own = self.owners[faceIndex]
                nei = self.neighbours[faceIndex]
                
                if iElement == own:
                    self.upperAnbCoeffIndex[faceIndex] = iNb
                elif iElement == nei:
                    self.lowerAnbCoeffIndex[faceIndex] = iNb
                    
                iNb = iNb +1


    def cfdProcessNodeTopology(self):
        
        self.nodeElements = self.cfdInvertConnectivity(self.elementNodes)
        self.nodeFaces = self.cfdInvertConnectivity(self.faceNodes) 
        
        
    def cfdInvertConnectivity(self,theConnectivityArray):
        
        
        theInvertedSize=0
        
        for i in range(len(theConnectivityArray)):
            for j in range(len(theConnectivityArray[i])):
                
                theInvertedSize=max(theInvertedSize, int(theConnectivityArray[i][j]))
        
        theInvertedConnectivityArray = [[] for i in range(theInvertedSize+1)]
        
        for i in range(len(theConnectivityArray)):
            for j in range(len(theConnectivityArray[i])):
                theInvertedConnectivityArray[int(theConnectivityArray[i][j])].append(i)
    
        return theInvertedConnectivityArray        
        
        
    def cfdProcessGeometry(self):
        """This function processes the mesh geometry"""
    
    #    self.faceCentroids']= [[] for i in range(self.numberOfFaces'])]
    #    self.faceSf']= [[] for i in range(self.numberOfFaces'])]
    #    self.faceAreas']= [[] for i in range(self.numberOfFaces'])]
        
        self.faceWeights= [[0] for i in range(self.numberOfFaces)]
        self.faceCF= [[0, 0, 0] for i in range(self.numberOfFaces)]
        self.faceCf= [[0,0,0] for i in range(self.numberOfFaces)]
        self.faceFf= [[0,0,0] for i in range(self.numberOfFaces)]
        self.wallDist= [[] for i in range(self.numberOfFaces)]
        self.wallDistLimited= [[] for i in range(self.numberOfFaces)]
        
        self.elementCentroids= [[] for i in range(self.numberOfElements)]
        self.elementVolumes= [[] for i in range(self.numberOfElements)]
        
        """
        Calculate:
            -face centroids (faceCentroids)
            -face normal (Sf)
            -face areas (faceAreas)
        """
        
        #find cell with largest number of points
        maxPoints=len(max(self.faceNodes, key=len))
        forCross1 = [[] for i in range(maxPoints)]
        forCross2 = [[] for i in range(maxPoints)]
        local_faceCentroid=[[] for i in range(maxPoints)]
        
        for iFace in range(self.numberOfFaces):
            theNodeIndices = self.faceNodes[iFace]
            theNumberOfFaceNodes = len(theNodeIndices)
            
            #compute a rough centre of the face
            local_centre = [0,0,0]
            
            for iNode in theNodeIndices:
                local_centre = local_centre + self.nodeCentroids[int(iNode)]
        
            local_centre = local_centre/theNumberOfFaceNodes
        
            for iTriangle in range(theNumberOfFaceNodes):
                
                point1 = local_centre
                point2 = self.nodeCentroids[int(theNodeIndices[iTriangle])]
                
                if iTriangle < theNumberOfFaceNodes-1:
                    point3 = self.nodeCentroids[int(theNodeIndices[iTriangle+1])]
                else:
                    point3 = self.nodeCentroids[int(theNodeIndices[0])]
                
                local_faceCentroid[iTriangle].append((point1+point2+point3)/3)
                
                left=point2-point1
                right=point3-point1
                
                forCross1[iTriangle].append(left)
                forCross2[iTriangle].append(right)
            
        
        local_Sf=[np.zeros([self.numberOfFaces,3]) for i in range(maxPoints)]
        local_area=[np.zeros([self.numberOfFaces,3]) for i in range(maxPoints)]
        
        centroid=np.zeros([self.numberOfFaces,3])
        area=np.zeros([self.numberOfFaces])
        Sf=np.zeros([self.numberOfFaces,3])
        
        #cells with fewer faces than others are full of zeros
        for i in range(maxPoints):
            
            forCrossLeft=np.vstack(np.array(forCross1[i]))
            forCrossRight=np.vstack(np.array(forCross2[i]))
            
            local_Sf[i]=0.5*np.cross(forCrossLeft,forCrossRight)
            local_area[i]=np.linalg.norm(local_Sf[i],axis=1)
        
            centroid = centroid + np.array(local_faceCentroid[i])*local_area[i][:,None]
            Sf=Sf+local_Sf[i]
            area=area+local_area[i]
            
        self.faceCentroids=centroid/area[:,None]
        self.faceSf=Sf
        self.faceAreas=area   
        
        
        """
        Pure python version - causes slowness due to iterative np.cross()
        """
        
    #    for iFace in range(self.numberOfFaces):
    #        theNodeIndices = self.faceNodes[iFace]
    #        theNumberOfFaceNodes = len(theNodeIndices)
    #        
    #        #compute a rough centre of the face
    #        local_centre = [0,0,0]
    #        
    #        for iNode in theNodeIndices:
    #            
    #            local_centre = local_centre + self.nodeCentroids[int(iNode)]
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
    #            point2 = self.nodeCentroids[int(theNodeIndices[iTriangle])]
    #            
    #            if iTriangle < theNumberOfFaceNodes-1:
    #                point3 = self.nodeCentroids[int(theNodeIndices[iTriangle+1])]
    #            else:
    #                point3 = self.nodeCentroids[int(theNodeIndices[0])]
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
    #        self.faceCentroids[iFace]=centroid
    #        self.faceSf[iFace]=Sf
    #        self.faceAreas[iFace]=area
        
        
        """
        Calculate:
            -element centroids (elementCentroids)
            -element volumes (elementVolumes)
        """
        for iElement in range(self.numberOfElements):
            
            theElementFaces = self.elementFaces[iElement]
            
            #compute a rough centre of the element
            local_centre = [0,0,0]
            
            for iFace in range(len(theElementFaces)):
                faceIndex = theElementFaces[iFace]
                local_centre = local_centre + self.faceCentroids[faceIndex]
            
            local_centre = local_centre/len(theElementFaces)
            
            
            localVolumeCentroidSum = [0,0,0]
            localVolumeSum = 0
            
            for iFace in range(len(theElementFaces)):
                faceIndex = theElementFaces[iFace]
                
                Cf = self.faceCentroids[faceIndex]-local_centre
                
                faceSign = -1
                if iElement == self.owners[faceIndex]:
                    faceSign = 1
                    
                local_Sf = faceSign*self.faceSf[faceIndex]
                
                localVolume = np.dot(local_Sf,Cf)/3
                
                localCentroid = 0.75*self.faceCentroids[faceIndex]+0.25*local_centre
                
                localVolumeCentroidSum = localVolumeCentroidSum + localCentroid*localVolume
                
                localVolumeSum = localVolumeSum + localVolume
                
            self.elementCentroids[iElement]=localVolumeCentroidSum/localVolumeSum
            self.elementVolumes[iElement]=localVolumeSum
        
        
        for iFace in range(self.numberOfInteriorFaces):
            
            n=self.faceSf[iFace]/np.linalg.norm(self.faceSf[iFace])
            own=self.owners[iFace]
            nei = self.neighbours[iFace]
            
            self.faceCF[iFace]=self.elementCentroids[nei]-self.elementCentroids[own]
            self.faceCf[iFace]=self.faceCentroids[iFace]-self.elementCentroids[own]
            self.faceFf[iFace]=self.faceCentroids[iFace]-self.elementCentroids[nei]
            self.faceWeights[iFace]=(-np.dot(self.faceFf[iFace],n))/(-np.dot(self.faceFf[iFace],n)+np.dot(self.faceCf[iFace],n))
                
            
        for iBFace in range(self.numberOfInteriorFaces, self.numberOfFaces):
            
            
            n=self.faceSf[iBFace]/np.linalg.norm(self.faceSf[iBFace])
            own=self.owners[iBFace]
        
            self.faceCF[iBFace]=self.faceCentroids[iBFace]-self.elementCentroids[own]
            self.faceCf[iBFace]=self.faceCentroids[iBFace]-self.elementCentroids[own]  
            self.faceWeights[iBFace]=1
            self.wallDist[iBFace]= max(np.dot(self.faceCf[iBFace], n), 1e-24)
            self.wallDistLimited[iBFace]= max(self.wallDist[iBFace], 0.05*np.linalg.norm(self.faceCf[iBFace]))        
        
        
    def cfdGetBoundaryElementsSubArrayForBoundaryPatch(self):
        
        for iBPatch, theBCInfo in self.cfdBoundaryPatchesArray.items():
            
            startBElement=self.numberOfElements+self.cfdBoundaryPatchesArray[iBPatch]['startFaceIndex']-self.numberOfInteriorFaces
            endBElement=startBElement+self.cfdBoundaryPatchesArray[iBPatch]['numberOfBFaces']
        
            self.cfdBoundaryPatchesArray[iBPatch]['iBElements']=list(range(int(startBElement),int(endBElement)))        

    def cfdGetFaceCentroidsSubArrayForBoundaryPatch(self):
        
        for iBPatch, theBCInfo in self.cfdBoundaryPatchesArray.items():
            
            startBFace=self.cfdBoundaryPatchesArray[iBPatch]['startFaceIndex']
            endBFace=startBFace+self.cfdBoundaryPatchesArray[iBPatch]['numberOfBFaces']
            iBFaces=list(range(int(startBFace),int(endBFace))) 
        
            self.cfdBoundaryPatchesArray[iBPatch]['faceCentroids']=[self.faceCentroids[i] for i in iBFaces]

    def cfdGetOwnersSubArrayForBoundaryPatch(self):
        
        for iBPatch, theBCInfo in self.cfdBoundaryPatchesArray.items():
            
            startBFace=self.cfdBoundaryPatchesArray[iBPatch]['startFaceIndex']
            
            endBFace=startBFace+self.cfdBoundaryPatchesArray[iBPatch]['numberOfBFaces']
        
            iBFaces=list(range(int(startBFace),int(endBFace)))    
            
            self.cfdBoundaryPatchesArray[iBPatch]['owners_b']=[self.owners[i] for i in iBFaces]

    def cfdGetFaceSfSubArrayForBoundaryPatch(self):
        
        for iBPatch, theBCInfo in self.cfdBoundaryPatchesArray.items():
            
            startBFace=self.cfdBoundaryPatchesArray[iBPatch]['startFaceIndex']
            
            endBFace=startBFace+self.cfdBoundaryPatchesArray[iBPatch]['numberOfBFaces']
        
            iBFaces=list(range(int(startBFace),int(endBFace)))    
            
            self.cfdBoundaryPatchesArray[iBPatch]['facesSf']=[self.faceSf[i] for i in iBFaces]       
            
            self.cfdBoundaryPatchesArray[iBPatch]['facesSf']=np.asarray(self.cfdBoundaryPatchesArray[iBPatch]['facesSf'])


