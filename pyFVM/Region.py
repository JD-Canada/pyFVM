
import numpy as np

import pyFVM.IO as io
import pyFVM.FoamDictionaries as fd
import pyFVM.Polymesh as pm
import pyFVM.Equation as equation
import pyFVM.Field as field
import pyFVM.Interpolate as interpolate
import pyFVM.Coefficients as coefficients
import pyFVM.Fluxes as fluxes
import pyFVM.Gradient as grad
import pyFVM.Time as Time
import pyFVM.Assemble as assemble



class Region():

    """Sets up the simulation's 'Region'.

    An instance of the Region class is required for the case to run. 
    The instance is created at the beginning of each case and is used to hold
    other class instances, such as 'polyMesh', any number of 'fluid' instances
    and a number of other attributes required for the simulation to run.

    All information related to the mesh's topology (i.e., distances of cell centers to wall, face surface areas, face normals and cell volumes) is available in the Region class. 

    """

    def __init__(self,casePath):
        
        
        """Initiates the class instance with the caseDirectoryPath attribute 
        and adds the 'dictionaries' and 'fluid' dictionaries. Reminder - 
        __init__ functions are run automatically when a new class instance is 
        created. 
        """
        
        io.cfdPrintMainHeader()
        
        self.caseDirectoryPath = casePath
        self.STEADY_STATE_RUN = True

        print('Working case directory is %s' % self.caseDirectoryPath)
        
        ## Dictionary to hold 'fluid' properties. We are considering changing this to a more meaningful name such as 'field' because often this dictionary is used to store field and field variables which are not necessarily fluids.  
        self.fluid={}
        
        ## Dictionary to hold various equations
        self.model={}

        ## Dictionary holding information contained within the various c++ dictionaries used in OpenFOAM. For example, the contents of the './system/controlDict' file can be retrieved by calling Region.dictionaries.controlDict which return the dictionary containing all the entries in controlDict. 
        self.dictionaries=fd.FoamDictionaries(self)
        
        ## Dictionary containing all the information related to the FVM mesh. 
        self.mesh=pm.Polymesh(self)
        
        print('\n')

        """cfdGeometricLengthScale() and self.dictionaries.cfdReadTimeDirectory() require the mesh and therefore are not included in the __init__ function of FoamDictionaries and are instead called after the self.mesh=pm.Polymesh(self) line above."""
        
        self.cfdGeometricLengthScale()
        self.dictionaries.cfdReadTimeDirectory()
        
        #update boundary values
        for i in self.fluid:
            self.fluid[i].updateFieldForAllBoundaryPatches()
                
        self.dictionaries.cfdReadTransportProperties()
        self.dictionaries.cfdReadThermophysicalProperties()

        #Define transient-convection equation
        self.model['phi']=equation.Equation(self,'phi')
        self.model['phi'].setTerms(['Transient', 'Convection'])
        
        #Define mdot_f field
        self.fluid['mdot_f']=field.Field(self,'mdot_f','surfaceScalarField')
        self.fluid['mdot_f'].dimensions=[0,0,0,0,0,0,0]
        self.initializeMdotFromU()
        
        io.cfdPrintHeader()
        
        ## Instance of Coefficients class which contains information related to the connectivity of the mesh.
        self.coefficients=coefficients.Coefficients(self)

        ## Instance of Fluxes class which contains flux information  
        self.fluxes=fluxes.Fluxes(self)
        
        self.phiGradLinear=grad.Gradient(self,'phi')
        self.phiGradLinear.cfdComputeGradientGaussLinear0()

        self.UGradLinear=grad.Gradient(self,'U')
        self.UGradLinear.cfdComputeGradientGaussLinear0()
        
        #There is something wrong with cfdUpdateScale it is not giving the same numbers as uFVM
        self.fluid['phi'].cfdUpdateScale()

        self.time = Time.Time(self)
     
        io.cfdInitDirectories(self) 

        totalNumberOfIterations = 0
        
        while(self.time.cfdDoTransientLoop()):
            
            #manage time
            self.time.cfdPrintCurrentTime()
            self.time.cfdUpdateRunTime()
      
            # Copy current field into previous TIME field        
            self.thePhiField = self.fluid['phi']
            self.thePhiField.setPreviousTimeStep()
            

            #sub-loop
            for nIter in range(10):
                
                totalNumberOfIterations += 1
        
                io.cfdPrintInteration(totalNumberOfIterations)        
                io.cfdPrintResidualsHeader()
                
                #Previous iteration of self.fluid
                self.thePhiField.setPreviousTimeStep()
                
                """
                To-do: Work through cfdAssembleAndCorrectScalarEquation()
                """
                
                self.assembledPhi=assemble.Assemble(self,'phi')

     
    def cfdGeometricLengthScale(self):
    
        """
        Calculates the geometric length scale of the mesh. 
        Length scale = [sum(element volume)]^(1/3)
        """
    
        self.totalVolume = sum(self.mesh.elementVolumes)
        self.lengthScale = self.totalVolume**(1/3)
    

    def initializeMdotFromU(self):
        #not sure if this function fits here?
        
        U_f=interpolate.interpolateFromElementsToFaces(self,'linear','U')
        rho_f=np.squeeze(interpolate.interpolateFromElementsToFaces(self,'linear','rho'))
        Sf=self.mesh.faceSf
        
        #calculate mass flux through faces
        self.fluid['mdot_f'].phi=rho_f*(Sf*U_f).sum(1)
        

        