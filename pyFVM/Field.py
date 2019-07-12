import pyFVM.Math as mth
import sys


class Field():
    
    def __init__(self, Region,fieldName, fieldType):
        
        """Creates an empty field class that will be populated later on.
        
        Detects if field is either type volScalar, volVector, surfaceScalar, or 
        surfaceVector3 and creates an empty container with an adequate number of rows
        and columns (i.e., scalar = 1 column, vector = 3 columns) to hold field data.
        
        Attributes:
            
           
        Example usage:
            
            
        TODO:
        """
        
        self.Region=Region
        self.name = fieldName
        self.type = fieldType
        self.dimensions=[]
        self.boundaryPatchRef={}
        
        if self.type == 'volScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a volScalarField' % self.name)
        
        if self.type == 'volVectorField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi= [[0, 0, 0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a volVectorField' % self.name)
            
        if self.type == 'surfaceScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize = self.Region.mesh.numberOfBFaces
            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a surfaceScalarField' % self.name)
            
            
        if self.type == 'surfaceVector3Field':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize =self.Region.mesh.numberOfBFaces
            self.phi= [[0,0,0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('%s is a surfaceVector3Field' % self.name)
        
        #Previous iteration
        self.prevIter={}
        self.prevIter['phi']=self.phi
        
        #Previous time step
        self.prevTimeStep={}
        self.prevTimeStep['phi']=self.phi
        
        
        self.cfdUpdateScale()
        
        
        
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


    def cfdUpdateScalarFieldForAllBoundaryPatches(self):
        
        for iBPatch, theBCInfo in self.Region.mesh.cfdBoundaryPatchesArray.items():
            
            self.iBPatch = iBPatch #for using in other functions
            
            #boundary type for patch defined in 'boundary' file in polyMesh folder
            thePhysicalPatchType=theBCInfo['type']
            
            #boundary type defined for same patch in "0" file
            theBCType=self.boundaryPatchRef[iBPatch]['type']
            

            if thePhysicalPatchType == 'wall':
                
                if theBCType == 'fixedValue':
                    
                    self.cfdUpdateFixedValueScalar()
                    
                elif theBCType == 'zeroGradient' or thePhysicalPatchType == 'noSlip' or thePhysicalPatchType == 'slip' :
                    
                    self.cfdUpdateZeroGradientScalar()
                    
                else:
                    print('The %s patch type is ill defined or missing!' % iBPatch)
                
            elif thePhysicalPatchType == 'inlet':
                
                if theBCType == 'fixedValue':
                    
                    self.cfdUpdateFixedValueScalar()
                    
                elif theBCType == 'zeroGradient':
                    
                    self.cfdUpdateFixedValueSalar()
                    
                else:
                    print('The %s patch type is ill defined or missing!' % iBPatch)

            elif thePhysicalPatchType == 'outlet':
                
                if theBCType == 'fixedValue' :
                    
                    self.cfdUpdateFixedValueScalar()
                    
                elif theBCType == 'zeroGradient' or theBCType == 'outlet':
                    
                    self.cfdUpdateZeroGradientScalar()
                    
                else:
                    
                    print('The %s patch type is ill defined or missing!' % iBPatch)       
 

            elif thePhysicalPatchType == 'symmetry':
                
                self.cfdUpdateZeroGradientScalar()
                
            elif thePhysicalPatchType == 'empty':
                
                self.cfdUpdateZeroGradientScalar()                

            else:
                
                print('Physical condition bc not defined correctly for the %s patch in "boundary" file !' %iBPatch)
                sys.exit()


    def cfdUpdateFixedValueScalar(self):
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['iBElements']
        
        boundaryValue=self.boundaryPatchRef[self.iBPatch]['value']
               
        for index in iBElements:
            self.phi[index] = boundaryValue
        
        
    def cfdUpdateZeroGradientScalar(self):
        
        iBElements=self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['iBElements']
        
        #elements that own the boundary faces
        owners_b = self.Region.mesh.cfdBoundaryPatchesArray[self.iBPatch]['owners_b']
        
        newValues=[]
        
        for index in owners_b:
            newValues.append(self.phi[index])

        for count, index in enumerate(iBElements):

            self.phi[index]=newValues[count]
                
    
    
       