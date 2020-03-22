import numpy as np
import pyFVM.Math as mth


class Gradient():
    
    def __init__(self, Region, phiName):
        
        """
        Handles gradient calculations on the field specified by phiName. First,
        create an instance of the class, then call cfdComputeGradientGaussLinear0,
        which calculates the gradients at each cell. At the end of 
        cfdComputeGradientGaussLinear0, cfdUpdateGradient() is called which updates
        the gradients on the boundary faces.
        """
        
        self.Region=Region
        self.phiName=phiName
        self.phi=self.Region.fluid[phiName].phi
        self.type=self.Region.fluid[phiName].type
        
        theSize=self.phi.shape[1]
        
        if theSize == 3:
            self.theNumberOfComponents=3
        else:
            self.theNumberOfComponents=1
        
        #domain-wide variables
        self.elementCentroids=self.Region.mesh.elementCentroids
        self.theNumberOfElements=self.Region.mesh.numberOfElements
        
        #interior variables
        self.owners_f=self.Region.mesh.interiorFaceOwners
        self.neighbours_f=self.Region.mesh.interiorFaceNeighbours
        self.Sf=self.Region.mesh.interiorFaceSf
        self.g_f=self.Region.mesh.interiorFaceWeights
        self.iFaces=self.Region.mesh.numberOfInteriorFaces
        self.ones=np.ones((self.iFaces))
        self.phi_f=np.zeros((self.iFaces,self.theNumberOfComponents))

        #boundary variables
        self.boundaryPatches=self.Region.mesh.cfdBoundaryPatchesArray
        self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
        self.iBElements=np.arange(self.Region.mesh.numberOfElements,self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBFaces,1)
        self.phi_b=self.phi[self.iBElements]
        self.owners_b=self.Region.mesh.owners_b
        self.Sf_b=self.Region.mesh.Sf_b
        
        ## phiGrad array to hold gradient values at interior and boundary centroids. For scalars this array has shape (self.theNumberOfElements+self.theBoundaryArraySize,3,1) for vectors this array has shape (self.theNumberOfElements+self.theBoundaryArraySize,3,3)
        self.phiGrad=np.zeros((self.theNumberOfElements+self.theBoundaryArraySize, 3,self.theNumberOfComponents))

    def cfdUpdateGradient(self):

        """ Prints the boundary type and then assigns the calculated phiGrad field to self.Region.fluid[self.phiName].phiGrad

        """
        
        for patch, patchInfo in self.boundaryPatches.items():
            thePhysicalType =patchInfo['type']
            
            if thePhysicalType =='wall':
                print('This patch is of type %s' %thePhysicalType)
            elif thePhysicalType =='inlet':
                self.updateInletGradients(patch)
                print('This patch is of type %s' %thePhysicalType)
            elif thePhysicalType =='outlet':
                self.updateOutletGradients(patch)
                print('This patch is of type %s' %thePhysicalType)
            elif thePhysicalType =='symmetry' or 'empty':
                print('This patch is of type %s' %thePhysicalType)
            else:
                print('Boundary condition is not correctly spelled or unrecognized ...')
                
        self.Region.fluid[self.phiName].phiGrad=self.phiGrad                

    def cfdComputeGradientGaussLinear0(self):
        
        """ 
        This function computes the gradient for a field at the centroids of 
        the elements using a first order gauss interpolation. No correction for 
        non-conjuntionality is applied. 'phi' is the name of a field 
        used when the class is instantiated.
        
        To-do: Check this in-depth over a number of scenarios
        """
        
        #interior face contribution, treats vectors as three scalars (u,v,w)
        for iComponent in range(self.theNumberOfComponents):
            
            #vectorized linear interpolation (same as Interpolate.interpolateFromElementsToFaces('linear'))
            self.phi_f[0:self.iFaces,iComponent]=self.g_f*self.phi[self.neighbours_f][:,iComponent]+(self.ones-self.g_f)*self.phi[self.owners_f][:,iComponent]
            
            for iFace in range(self.iFaces):
                
                #this only updates phiGrad at the centroids of interior elements, the contribution of boundary faces to boundary centroids is done directly below. 
                
                #accumlator of phi_f*Sf for the owner centroid of the face  
                self.phiGrad[self.owners_f[iFace],:,iComponent]=self.phiGrad[self.owners_f[iFace],:,iComponent]+self.phi_f[iFace,iComponent]*self.Sf[iFace]
                
                #accumlator of phi_f*Sf for the neighbour centroid of the face  
                self.phiGrad[self.neighbours_f[iFace],:,iComponent]=self.phiGrad[self.neighbours_f[iFace],:,iComponent]-self.phi_f[iFace,iComponent]*self.Sf[iFace]

        #Boundary face contributions
        for iComponent in range(self.theNumberOfComponents):
            
            for iFace in range(self.Region.mesh.numberOfBFaces):
                self.phiGrad[self.owners_b[iFace],:,iComponent]=self.phiGrad[self.owners_b[iFace],:,iComponent]+self.phi_b[iFace,iComponent]*self.Sf_b[iFace]

        #calculate volume averaged gradient by dividing self.phiGrad by element volumes
        self.volumes = self.Region.mesh.elementVolumes
        for iComponent in range(self.theNumberOfComponents):
            for iElement in range(self.Region.mesh.numberOfElements):
                self.phiGrad[iElement,:,iComponent] = self.phiGrad[iElement,:,iComponent]/self.volumes[iElement]
            
        self.iBElements = np.arange(self.Region.mesh.numberOfElements, self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBFaces, dtype=int)
        
        self.phiGrad[self.iBElements,:,:] = self.phiGrad[self.owners_b,:,:]

        self.cfdUpdateGradient()

    def updateWallGradients(self,patch):

        """This function is written but has not been implemented yet in self.cfdUpdateGradient() above. The reason is because the test case we are using to check the code with does not have a wall boundary. I get it, I am lazy, but when we do have a wall boundary we will need to verify that this code is indeed working as intending by comparing its output to uFVM.
        """
        
        owners_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['owners_b']
        faceCentroids_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['faceCentroids']
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[patch]['iBElements']
        
        numberOfBFaces = self.Region.mesh.cfdBoundaryPatchesArray[patch]['numberOfBFaces']
        startBFace = self.Region.mesh.cfdBoundaryPatchesArray[patch]['startFaceIndex']
        
        startBElement = startBFace - self.iFaces + self.theNumberOfElements
        endBElement = startBElement + numberOfBFaces-1
        
        grad_b=np.zeros((numberOfBFaces, 3,self.theNumberOfComponents))
        
        for iComponent in range(self.theNumberOfComponents):
            for iBFace in range(numberOfBFaces):
                iBElement = startBElement+iBFace
                iOwner = owners_b[iBFace]
                
                Cf=faceCentroids_b[iBFace]
                C = self.elementCentroids[iOwner]
                dCf=Cf-C
                e=dCf/mth.cfdMag(dCf)
                
                grad_b[iBFace,:,iComponent] = self.phiGrad[iOwner,:,iComponent] - (self.phiGrad[iOwner,:,iComponent]*e)*e + ((self.phi[iBElement,iComponent] - self.phi[iOwner,iComponent])/mth.cfdMag(dCf))*e;

        self.phiGrad[iBElements,:,:]=grad_b       
                
   
    def updateInletGradients(self,patch):
        
        owners_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['owners_b']
        faceCentroids_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['faceCentroids']
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[patch]['iBElements']
        
        numberOfBFaces = self.Region.mesh.cfdBoundaryPatchesArray[patch]['numberOfBFaces']
        startBFace = self.Region.mesh.cfdBoundaryPatchesArray[patch]['startFaceIndex']
        
        startBElement = startBFace - self.iFaces + self.theNumberOfElements
        endBElement = startBElement + numberOfBFaces-1
        
        grad_b=np.zeros((numberOfBFaces, 3,self.theNumberOfComponents))
        
        for iComponent in range(self.theNumberOfComponents):
            for iBFace in range(numberOfBFaces):
                iBElement = startBElement+iBFace
                iOwner = owners_b[iBFace]
                
                Cf=faceCentroids_b[iBFace]
                C = self.elementCentroids[iOwner]
                dCf=Cf-C
                e=dCf/mth.cfdMag(dCf)
                
                grad_b[iBFace,:,iComponent] = self.phiGrad[iOwner,:,iComponent] - (self.phiGrad[iOwner,:,iComponent]*e)*e + ((self.phi[iBElement,iComponent] - self.phi[iOwner,iComponent])/mth.cfdMag(dCf))*e;

        self.phiGrad[iBElements,:,:]=grad_b       
                
    def updateOutletGradients(self,patch):
        
        owners_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['owners_b']
        faceCentroids_b=self.Region.mesh.cfdBoundaryPatchesArray[patch]['faceCentroids']
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[patch]['iBElements']
        
        numberOfBFaces = self.Region.mesh.cfdBoundaryPatchesArray[patch]['numberOfBFaces']
        startBFace = self.Region.mesh.cfdBoundaryPatchesArray[patch]['startFaceIndex']
        
        startBElement = startBFace - self.iFaces + self.theNumberOfElements
        endBElement = startBElement + numberOfBFaces-1
        
        grad_b=np.zeros((numberOfBFaces, 3,self.theNumberOfComponents))        
        
        for iComponent in range(self.theNumberOfComponents):
            for iBFace in range(numberOfBFaces):
                iBElement = startBElement+iBFace
                iOwner = owners_b[iBFace]
                
                Cf=faceCentroids_b[iBFace]
                C = self.elementCentroids[iOwner]
                dCf=Cf-C
                e=dCf/mth.cfdMag(dCf)
                
                grad_b[iBFace,:,iComponent] = self.phiGrad[iOwner,:,iComponent] - (self.phiGrad[iOwner,:,iComponent]*e)*e + ((self.phi[iBElement,iComponent] - self.phi[iOwner,iComponent])/mth.cfdMag(dCf))*e;

        self.phiGrad[iBElements,:,:]=grad_b 


    def cfdGetGradientSubArrayForInterior(self):

        if self.type == "surfaceScalarField":
              self.phiGradInter=self.phiGrad[0:self.region.mesh.numberOfInteriorFaces]

        