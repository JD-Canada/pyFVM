import pyFVM.Math as mth


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
        
        if self.type == 'volScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('volScalarField read')
        
        if self.type == 'volVectorField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfElements
            self.theBoundaryArraySize = self.Region.mesh.numberOfBElements
            self.phi= [[0, 0, 0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('volVectorField read')
            
        if self.type == 'surfaceScalarField':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize = self.Region.mesh.numberOfBFaces
            self.phi= [[0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('surfaceScalarField read')  
            
        if self.type == 'surfaceVector3Field':
            
            self.theInteriorArraySize = self.Region.mesh.numberOfInteriorFaces
            self.theBoundaryArraySize =self.Region.mesh.numberOfBFaces
            self.phi= [[0,0,0] for i in range(self.theInteriorArraySize+self.theBoundaryArraySize)]
            print('surfaceVector3Field read')    
        
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
#        print(self.phi)
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
#            print('mag')
#            print(theMagnitude)
            phiScale = max(self.Region.lengthScale,phiMax)
            
        else: 
            
            phiScale = phiMax
    
        self.max=phiMax
        self.min=phiMin
        self.scale=phiScale

        