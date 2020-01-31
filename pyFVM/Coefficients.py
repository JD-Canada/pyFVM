import numpy as np

class Coefficients():
    
    def __init__(self,Region):
        
        self.region=Region
        self.setupCoefficients()

    def setupCoefficients(self,**kwargs):
        
        #uFVM has different levels within their Region.coefficients.
        #I am not sure why, but we might need to add some functionality to 
        #hold all these in different levels later on ...
    
        if len(kwargs)==0:
            
            #coefficient connectivity and sizes
            theCConn = self.region.mesh.elementNeighbours
            theCSize = np.zeros((len(theCConn)))
            
            for iElement,value in enumerate(theCConn):
                theCSize[iElement]=len(theCConn[iElement])
               
        theNumberOfElements=len(theCConn)
        
        self.ac=np.zeros((theNumberOfElements))
        self.ac_old=np.zeros((theNumberOfElements))
        self.bc=np.zeros((theNumberOfElements))
        
        self.anb=[]
        
        for iElement in range(theNumberOfElements):
            
            #easiest way to make a list of zeros of defined length ...
            listofzeros = [0]*int(theCSize[iElement])
            self.anb.append(listofzeros)
        
        self.dc=np.zeros((theNumberOfElements))
        self.rc=np.zeros((theNumberOfElements))
        
        self.dphi=np.zeros((theNumberOfElements))
        
        self.cconn=theCConn
        self.csize=theCSize