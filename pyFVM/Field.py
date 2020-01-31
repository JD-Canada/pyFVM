import numpy as np
import sys

import pyFVM.Math as mth


class Field():
    
    def __init__(self, Region,fieldName, fieldType):
        
        """Creates an empty field class that will be populated later on.
        
        Detects if field is either type volScalar, volVector, surfaceScalar, or 
        surfaceVector3 and creates an empty container with an adequate number of rows
        and columns (i.e., scalar = 1 column, vector = 3 columns) to hold field data.
        
        Attributes:
            
           
        Example usage:
            
        """
        
        self.Region=Region
        self.name = fieldName
        self.type = fieldType
        self.dimensions=[]
        self.boundaryPatchRef={}
        
        if self.type == 'volScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi = np.zeros((self.theInteriorArraySize+self.theBoundaryArraySize, 1))
#            self.phi_f = np.zeros((self.Region.mesh.numberOfFaces, 1))
#            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a volScalarField' % self.name)
        
        if self.type == 'volVectorField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi = np.zeros((self.theInteriorArraySize+self.theBoundaryArraySize, 3))
#            self.phi_f = np.zeros((self.Region.mesh.numberOfFaces, 3))
#            self.phi= [[0, 0, 0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a volVectorField' % self.name)
            
        if self.type == 'surfaceScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize = self.Region.mesh.numberOfBFaces
            self.phi = np.zeros((self.theInteriorArraySize+self.theBoundaryArraySize, 1))
#            self.phi_f = np.zeros((self.Region.mesh.numberOfFaces, 1))
#            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a surfaceScalarField' % self.name)
            
        if self.type == 'surfaceVector3Field':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize =self.Region.mesh.numberOfBFaces
            self.phi = np.zeros((self.theInteriorArraySize+self.theBoundaryArraySize, 3))
#            self.phi_f = np.zeros((self.Region.mesh.numberOfFaces, 3))
#            self.phi= [[0,0,0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a surfaceVector3Field' % self.name)
        
        #Previous iteration
        self.prevIter={}
        self.prevIter['phi']=self.phi
        
        #Previous time step
        self.prevTimeStep={}
        self.prevTimeStep['phi']=self.phi
        
        self.cfdUpdateScale()
        
        self.phiGrad=[]
        
        

        
        
        
    def cfdUpdateScale(self):
    
        """Update the min, max and scale values of a field in Region
        Attributes:
            
           Region (str): the cfd Region.
           field (str): the field in Region.fields
           
        Example usage:
            
            cfdUpdateScale(Region,'rho')
        """    

        theMagnitude = mth.cfdMag(self.phi)
        
   
        try:
            
            #see if it is a vector
            iter(theMagnitude)
            phiMax=max(mth.cfdMag(self.phi))
            phiMin=min(mth.cfdMag(self.phi))
            print(phiMax)
    
        except TypeError:
            
            #knows it is scalar, so ...
            phiMax=theMagnitude
            phiMin=theMagnitude

        if self.name=='p':
            
            #!!!! the 'scale' variable for p doesn't exist yet
            vel_scale = self.Region.fluid['p'].scale
            rho_scale = self.Region.fluid['rho'].scale
            p_dyn = 0.5 * rho_scale * vel_scale^2
            phiScale = max(phiMax,p_dyn)
    
        elif self.name=='U':
            phiScale = max(self.Region.lengthScale,phiMax)
            
        else: 
            
            phiScale = phiMax
    
        self.max=phiMax
        self.min=phiMin
        self.scale=phiScale


    def setDimensions(self,dimensions):
        
        self.dimensions=dimensions


    def updateFieldForAllBoundaryPatches(self):
        
        for iBPatch, theBCInfo in self.Region.mesh.cfdBoundaryPatchesArray.items():
            
            self.iBPatch = iBPatch #for using in other functions
            
            #boundary type for patch defined in 'boundary' file in polyMesh folder
            thePhysicalPatchType=theBCInfo['type']
            
            #boundary type defined for same patch in "0" file
            theBCType=self.boundaryPatchRef[iBPatch]['type']
            
            
            if thePhysicalPatchType == 'wall':
                
                if theBCType == 'fixedValue':
                    
                    if self.type == 'volScalarField':
                        self.updateFixedValue()
                    if self.type == 'volVectorField':
                        self.updateFixedValue()
                    
                elif theBCType == 'zeroGradient' or thePhysicalPatchType == 'noSlip' or thePhysicalPatchType == 'slip' :
                    
                    if self.type == 'volScalarField':
                        self.updateZeroGradient()
                    if self.type == 'volVectorField':
                        self.updateZeroGradient()
                else:
                    print('The %s patch type is ill defined or missing!' % iBPatch)
                
            elif thePhysicalPatchType == 'inlet':
                
                if theBCType == 'fixedValue':
                    if self.type == 'volScalarField':
                        self.updateFixedValue()
                    if self.type == 'volVectorField':
                        self.updateFixedValue() 
                    
                elif theBCType == 'zeroGradient':
                    if self.type == 'volScalarField':
                        self.updateFixedValue()
                    if self.type == 'volVectorField':
                        self.updateFixedValue() 
                else:
                    print('The %s patch type is ill defined or missing!' % iBPatch)

            elif thePhysicalPatchType == 'outlet':
                
                if theBCType == 'fixedValue' :
                    if self.type == 'volScalarField':
                        self.updateFixedValue()
                    if self.type == 'volVectorField':
                        self.updateFixedValue()
                        
                elif theBCType == 'zeroGradient' or theBCType == 'outlet':
                    
                    if self.type == 'volScalarField':
                        self.updateZeroGradient()
                    if self.type == 'volVectorField':
                        self.updateZeroGradient()
                else:
                    print('The %s patch type is ill defined or missing!' % iBPatch)       
 
            elif thePhysicalPatchType == 'symmetry':
                
                if self.type == 'volScalarField':
                    self.updateZeroGradient()
                if self.type == 'volVectorField':
                    self.updateSymmetry()
                    
            elif thePhysicalPatchType == 'empty':
                
                if self.type == 'volScalarField':
                    self.updateZeroGradient()
                if self.type == 'volVectorField':
                    self.updateSymmetry()

            else:
                print('Physical condition bc not defined correctly for the %s patch in "boundary" file !' %iBPatch)
                sys.exit()


    def updateFixedValue(self):
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['iBElements']
        
        self.phi[iBElements] = self.boundaryPatchRef[self.iBPatch]['value']
        
        
    def updateZeroGradient(self):
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['iBElements']
        
        #elements that own the boundary faces
        owners_b = self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['owners_b']
        
        newValues=[]
        
        for index in owners_b:
            newValues.append(self.phi[index])

        for count, index in enumerate(iBElements):
            self.phi[index]=newValues[count]
                
    
    def updateSymmetry(self):
        
        #get indices for self.iBPatch's boundary faces in self.phi array
        self.iBElements=self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['iBElements']
        
        #get indices for the owners (i.e. cells) for self.iBPatch's boundary faces in self.phi array 
        self.owners_b = self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['owners_b']
        
        #get vector (direction in which the face points) for self.iBpatch's boundary faces 
        self.Sb = self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['facesSf']
        
        #normalize Sb vector
        self.normSb = mth.cfdMag(self.Sb)
        
        #normalize Sb components and horizontally stack them into the columns of array n
        self.n=np.column_stack((self.Sb[:,0]/self.normSb,self.Sb[:,1]/self.normSb,self.Sb[:,2]/self.normSb))
        
        #perform elementwise multiplication of owner's values with boundary face normals
        self.U_normal_cfdMag=(self.phi[self.owners_b]*self.n).sum(1)
        
        #seems to do the same thing a the above line without the .sum(1)
        self.U_normal=np.column_stack((self.U_normal_cfdMag*self.n[:,0],self.U_normal_cfdMag*self.n[:,1],self.U_normal_cfdMag*self.n[:,2]))
        
        
        self.phi[self.iBElements]=self.phi[self.owners_b]-self.U_normal
        
        
# I'm not sure these functions belong to the field class, they just bring up info of an already existing field
def cfdGetSubArrayForInterior(self,theFieldName,*args):

    
    if self.fluid[theFieldName].type == 'surfaceScalarField':
        phi = self.fluid[theFieldName].phi[0:self.mesh.numberOfInteriorFaces]
       
    elif self.fluid[theFieldName].type == 'volScalarField':
        phi = self.fluid[theFieldName].phi[0:self.mesh.numberOfElements]    
        
    elif self.fluid[theFieldName].type == 'volVectorField':
        if args:
            iComponent = args
            phi = self.fluid[theFieldName].phi[0:self.mesh.numberOfElements, iComponent] 
        else:
            phi = self.fluid[theFieldName].phi[0:self.mesh.numberOfElements, :] 

    return phi
        

def cfdGetPrevTimeStepSubArrayForInterior(self,theFieldName,*args):

    
    if not args:
        iComponent = 0
    else:
        iComponent = args[0]
        
    if self.fluid[theFieldName].type == 'scfdUrfaceScalarField':
        phi = self.prevTimeStep[theFieldName].phi[0:self.mesh.numberOfInteriorFaces]
    else:
        phi = self.prevTimeStep[theFieldName].phi[0:self.mesh.numberOfElements,iComponent]
    
    return phi