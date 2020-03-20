import numpy as np
import pyFVM.Field as field

class Assemble:
    """Logic and functions necessary to assemble an equation 
    """

    def __init__(self,Region,theEquationName):
        """ Initiates the Assemble class instance
        """

        ## Instance of the case's region class
        self.region=Region

        ## Name of the equation stored in region.model dictionary
        self.theEquationName=theEquationName

        ## The instance of Equation stored in the self.region.model dictionary
        self.theEquation=self.region.model[self.theEquationName]
        
        self.cfdPreAssembleEquation()
        self.cfdAssembleEquationTerms()
        

    def cfdPreAssembleEquation(self):
        #empty in uFVM
        pass

    def cfdAssembleEquationTerms(self): 
        """
        Assembles the equation's terms
        """
        
        print('Inside cfdAssembleEquationTerms')
       
        for iTerm in self.theEquation.terms:

            if iTerm == 'Transient':
                self.cfdZeroElementFLUXCoefficients()
                self.cfdAssembleTransientTerm()
#                self.cfdAssembleIntoGlobalMatrixElementFluxes()
                
            elif iTerm == 'Convection':
                print('It is convection')

            elif iTerm == 'Diffusion':
                print('It is diffusion')

            elif iTerm == 'FalseTransient':
                print('It is false transient')
                
            else:
                print('\n%s\n' % (iTerm + ' term is not defined'))


        self.cfdAssembleConvectionTermInterior('phi')

    def cfdZeroElementFLUXCoefficients(self):
        """
        Sets the coefficient arrays equal to zero
        """
        
        print('Inside cfdZeroElementFLUXCoefficients')
        self.region.fluxes.FluxC.fill(0)
        self.region.fluxes.FluxV.fill(0)
        self.region.fluxes.FluxT.fill(0)
        self.region.fluxes.FluxC_old.fill(0)

    def cfdAssembleTransientTerm(self):

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
        
        print('Inside cfdAssembleTransientTerm')
        
        theScheme = self.region.dictionaries.fvSchemes['ddtSchemes']['default']
        
        if theScheme == 'steadyState':
            pass
        elif theScheme == 'Euler':
            self.assembleFirstOrderEulerTransientTerm()
        else:
            print('\n%s' % (theScheme+' ddtScheme is incorrect'))


    def assembleFirstOrderEulerTransientTerm(self):
        
        """Assembles first order transient euler term
        """

        ## numpy array of element volumes
        self.volumes = np.asarray(self.region.mesh.elementVolumes).reshape(-1,1)   
        
       
        self.region.fluid[self.theEquationName].cfdGetSubArrayForInterior()
        self.region.fluid[self.theEquationName].cfdGetPrevTimeStepSubArrayForInterior()
        
        ## phi for interior
        self.phi=self.region.fluid[self.theEquationName].phiInteriorSubArray
        
        ## phi for interior in previous time step
        self.phi_old=self.region.fluid[self.theEquationName].phi_oldInteriorSubArray

        self.region.fluid['rho'].cfdGetSubArrayForInterior()
        self.region.fluid['rho'].cfdGetPrevTimeStepSubArrayForInterior()
        
        ## rho for interior
        self.rho=self.region.fluid['rho'].phiInteriorSubArray
        
        ## rho for interior in previous time step
        self.rho_old=self.region.fluid['rho'].phi_oldInteriorSubArray

        ## time step
        self.deltaT = self.region.dictionaries.controlDict['deltaT']
        
        
        local_FluxC = np.squeeze(np.multiply(self.volumes,np.divide(self.rho,self.deltaT)))
        local_FluxC_old = np.squeeze(np.multiply(-self.volumes,np.divide(self.rho_old,self.deltaT)))
        local_FluxV = np.zeros(len(local_FluxC))
        
        local_FluxT = np.squeeze(np.multiply(local_FluxC,np.squeeze(self.phi))) + np.multiply(local_FluxC_old,np.squeeze(self.phi_old))

        self.region.fluxes.FluxC = local_FluxC
        self.region.fluxes.FluxC_old = local_FluxC_old
        self.region.fluxes.FluxV = local_FluxV
        self.region.fluxes.FluxT = local_FluxT


    def cfdPostAssembleScalarEquation(self, theEquationName):
        """Empty function, not sure why it exists
        """
        pass

    def cfdAssembleConvectionTermInterior(self, theEquationName):
        
        numberOfInteriorFaces = self.region.mesh.numberOfInteriorFaces
        
        owners_f = self.region.mesh.interiorFaceOwners
        neighbours_f = self.region.mesh.interiorFaceNeighbours

        self.region.fluid[theEquationName].cfdGetSubArrayForInterior()
        phi=self.region.fluid[theEquationName].phiInteriorSubArray
        
        self.region.fluid['mdot_f'].cfdGetSubArrayForInterior()
        mdot_f=self.region.fluid['mdot_f'].phiInteriorSubArray
        
        local_FluxCf=np.maximum(mdot_f,0)
        local_FluxFf=-np.maximum(-mdot_f,0)
        
        local_FluxVf=np.zeros(len(local_FluxCf))
        
        self.region.fluxes.FluxCf[0:numberOfInteriorFaces] = local_FluxCf
        self.region.fluxes.FluxFf[0:numberOfInteriorFaces] = local_FluxFf
        self.region.fluxes.FluxVf[0:numberOfInteriorFaces] = local_FluxVf

        self.region.fluxes.FluxTf[0:numberOfInteriorFaces] = np.multiply(local_FluxCf,np.squeeze(phi[owners_f]))+ np.multiply(local_FluxFf,np.squeeze(phi[neighbours_f]))+ local_FluxVf
        
        
        
    def cfdAssembleIntoGlobalMatrixElementFluxes(self):
        """
        Add the face and volume contributions to obtain ac, bc and ac_old
        
        These are the ac and bc coefficients in the linear system of equations
        """
        
        
        self.region.coefficients.ac=self.region.coefficients.ac+self.region.fluxes.FluxC
        self.region.coefficients.ac_old=self.region.coefficients.ac_old+self.region.fluxes.FluxC_old
        self.region.coefficients.bc=self.region.coefficients.bc-self.region.fluxes.FluxT




        

        
                
        
    

    

