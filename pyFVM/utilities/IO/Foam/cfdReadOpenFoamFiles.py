from pyFVM.utilities.IO.Foam.cfdReadControlDictFile import cfdReadControlDictFile
from pyFVM.utilities.IO.Foam.cfdReadFvSchemesFile import cfdReadFvSchemesFile
from pyFVM.utilities.IO.Foam.cfdReadFvSolutionFile import cfdReadFvSolutionFile
from pyFVM.utilities.IO.Foam.cfdReadPolyMesh import cfdReadPolyMesh

def cfdReadOpenFoamFiles(Region):
    
    #reads in constant/polyMesh and processes mesh topology
    cfdReadPolyMesh(Region)

    #reads files in system/ folder 
    Region.foamDictionary['controlDict']=cfdReadControlDictFile(Region.caseDirectoryPath)
    Region.foamDictionary['fvSchemes']=cfdReadFvSchemesFile(Region.caseDirectoryPath)
    Region.foamDictionary['fvSolution']=cfdReadFvSolutionFile(Region.caseDirectoryPath)
    
    
    """
    TO-DO:
    
        -add in the following file read functions
    """
    
    #cfdReadTimeDirectory()
    
    #cfdReadTransportProperties()
    
    #cfdReadThermophysicalProperties()
    
    #cfdReadTurbulenceProperties()
    
    #cfdReadGravity()
    