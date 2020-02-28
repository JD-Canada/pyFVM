import numpy as np
import pyFVM.Field as field

"""
This file contains functions to assemble the transient term
"""

def cfdAssembleTransientTerm(self,theEquationName):

    """Chooses time-stepping approach

    If ddtSchemes is 'steadyState' then pass, if 'Euler' then redirect
    towards assembleFirstOrderEulerTransientTerm() or potentially others
    later on.

    Args:
        self (class instance): Instance of Region class.
        theEquationName (str): Equation (or field) name for which the transient terms will be assembled.

    Returns:
        none
    """
    
    theScheme = self.dictionaries.fvSchemes['ddtSchemes']['default']
    
    if theScheme == 'steadyState':
        pass
    elif theScheme == 'Euler':
        assembleFirstOrderEulerTransientTerm(self, theEquationName)
    else:
        print('\n%s' % (theScheme+' ddtScheme is incorrect'))
        
            
def assembleFirstOrderEulerTransientTerm(self, theEquationName):

    """Populates fluxes 
    """
    volumes = np.asarray(self.mesh.elementVolumes).reshape(-1,1)   
    
    # get fields
    phi = field.cfdGetSubArrayForInterior(self,theEquationName)
    phi_old = field.cfdGetPrevTimeStepSubArrayForInterior(self,theEquationName)
    
    rho = field.cfdGetSubArrayForInterior(self,'rho')
    rho_old = field.cfdGetPrevTimeStepSubArrayForInterior(self,'rho')
    
    deltaT = self.dictionaries.controlDict['deltaT']
    
    # local fluxes
    
    local_FluxC = np.multiply(volumes,np.divide(rho,deltaT))
    
    local_FluxC_old = np.multiply(-volumes,np.divide(rho_old,deltaT))
    
    local_FluxV = np.zeros(len(local_FluxC))
    
    local_FluxT = np.multiply(local_FluxC,phi) + np.multiply(local_FluxC_old,phi_old)

    self.fluxes.FluxC = local_FluxC
    self.fluxes.FluxC_old = local_FluxC_old
    self.fluxes.FluxV = local_FluxV
    self.fluxes.FluxT = local_FluxT
    

