import numpy as np

class Fluxes():
    
    def __init__(self,Region):
        
        self.region=Region
        self.setupFluxes()

    def setupFluxes(self,**kwargs):
        
        theNumberOfFaces=self.region.mesh.numberOfFaces
        theNumberOfElements=self.region.mesh.numberOfElements
        
        #face fluxes
        
        ## face flux linearization coefficients for cell C (cell of interest)
        self.FluxCf=np.zeros((theNumberOfFaces))
        
        ## face flux linearization coefficients for neighbouring cell
        self.FluxFf=np.zeros((theNumberOfFaces))
        
        ## non-linear face coefficients 
        self.FluxVf=np.zeros((theNumberOfFaces))
        
        ## total face flux (equal to FluxCf*phiC+FluxFf*phiF+FluxVf)
        self.FluxTf=np.zeros((theNumberOfFaces))

        #Volume fluxes (treated as source terms)
        self.FluxC=np.zeros((theNumberOfElements))
        
        ## volume flux equal to source value times cell volume (Q_{C}^{phi} * Vc)
        self.FluxV=np.zeros((theNumberOfElements))
        self.FluxT=np.zeros((theNumberOfElements))

        ## volume fluxes from previous time step
        self.FluxC_old=np.zeros((theNumberOfElements))