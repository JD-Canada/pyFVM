import numpy as np

def cfdZeroElementFLUXCoefficients(self):
    theNumberOfElements = self.mesh.numberOfElements

    self.fluxesFluxC = np.zeros((theNumberOfElements,))
    self.fluxesFluxV = np.zeros((theNumberOfElements,))
    self.fluxesFluxT = np.zeros((theNumberOfElements,))    

    self.fluxesFluxC_old = np.zeros((theNumberOfElements,))
