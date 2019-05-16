from pyFVM.utilities.IO.Foam.cfdReadControlDictFile import cfdReadControlDictFile
from pyFVM.utilities.IO.Foam.cfdReadFvSchemesFile import cfdReadFvSchemesFile
from pyFVM.utilities.IO.Foam.cfdReadFvSolutionFile import cfdReadFvSolutionFile


def cfdReadOpenFoamFiles(Region):
    
    Region.foamDictionary['controlDict']=cfdReadControlDictFile(Region.caseDirectoryPath)
    Region.foamDictionary['fvSchemes']=cfdReadFvSchemesFile(Region.caseDirectoryPath)
    Region.foamDictionary['fvSolution']=cfdReadFvSolutionFile(Region.caseDirectoryPath)