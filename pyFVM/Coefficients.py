import numpy as np

class Coefficients():
    
    def __init__(self,Region):
        
        ## local attribute of simulation's region instance
        self.region=Region
        self.setupCoefficients()

    def setupCoefficients(self,**kwargs):
        """Setups empty arrays containing the coefficients (ac and bc) required to solve the system of equations
        """
        
    
        if len(kwargs)==0:
            
            ## (list of lists) identical to polyMesh.elementNeighbours. Provides a list where each index represents an element in the domain. Each index has an associated list which contains the elements for which is shares a face (i.e. the neighouring elements).
            self.theCConn = self.region.mesh.elementNeighbours
            
            ## array containing the number of neighbouring elements for each element in the domain
            self.theCSize = np.zeros((len(self.theCConn)))
            
            for iElement,value in enumerate(self.theCConn):
                self.theCSize[iElement]=len(self.theCConn[iElement])
               
        theNumberOfElements=len(self.theCConn)
        
        ## array of cell-centered contribution to the flux term. These are constants and constant diffusion coefficients and therefore act as 'coefficients' in the algebraic equations. See p. 229 Moukalled.
        self.ac=np.zeros((theNumberOfElements))
        
        ## see ac, however this is for the previous timestep? Check this later when you know more. 
        self.ac_old=np.zeros((theNumberOfElements))
        
        ## array of the boundary condition contributions to the flux term.
        self.bc=np.zeros((theNumberOfElements))
        
        self.anb=[]
        
        for iElement in range(theNumberOfElements):
            
            #easiest way to make a list of zeros of defined length ...
            listofzeros = [0]*int(self.theCSize[iElement])
            self.anb.append(listofzeros)
        
        self.dc=np.zeros((theNumberOfElements))
        self.rc=np.zeros((theNumberOfElements))
        
        self.dphi=np.zeros((theNumberOfElements))
        