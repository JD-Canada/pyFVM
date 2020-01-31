import numpy as np

class Fluxes():
    
    def __init__(self,Region):
        
        self.region=Region
        self.setupFluxes()

    def setupFluxes(self,**kwargs):
        
        theNumberOfFaces=self.region.mesh.numberOfFaces
        theNumberOfElements=self.region.mesh.numberOfElements
        
        #face fluxes
        self.FluxCf=np.zeros((theNumberOfFaces))
        self.FluxFf=np.zeros((theNumberOfFaces))
        self.FluxVf=np.zeros((theNumberOfFaces))
        self.FluxTf=np.zeros((theNumberOfFaces))

        #Volume fluxes
        self.FluxC=np.zeros((theNumberOfElements))
        self.FluxV=np.zeros((theNumberOfElements))
        self.FluxT=np.zeros((theNumberOfElements))

        self.FluxC_old=np.zeros((theNumberOfElements))