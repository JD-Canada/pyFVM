import numpy as np 
import time
import os

from pyFVM.utilities.IO.Foam.cfdReadPolyMesh import cfdReadPolyMesh
from pyFVM.src.region.cfdSetupRegion import cfdSetupRegion
from pyFVM.utilities.print.cfdPrintMainHeader import cfdPrintMainHeader

from pyFVM.utilities.IO.Foam.cfdReadOpenFoamFiles import cfdReadOpenFoamFiles



#Region is the main data container for a case
cfdPrintMainHeader()

Region=cfdSetupRegion()
cfdReadOpenFoamFiles(Region)
cfdReadPolyMesh(Region)

a=Region.mesh

#start = time.time()
#stop=time.time()
#print(stop-start)

"""
Development code to include in cfdReadTimeDirectory.py

Next step:
    
    continue on line 92 of cfdReadTimeDirectory
    
"""
from pyFVM.src.time.cfdGetTimeSteps import cfdGetTimeSteps
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary
from pyFVM.utilities.IO.File.cfdGetFoamFileHeader import cfdGetFoamFileHeader
from pyFVM.src.fields.cfdSetupMeshField import cfdSetupMeshField

a=Region.mesh

contents=cfdReadTimeDirectory(Region)


my new code



def cfdReadTimeDirectory(Region,**kwargs):
    
    if len(kwargs) > 0:
        timeDirectory=kwargs['time']
        
        
    elif Region.foamDictionary['controlDict']['startFrom']=='startTime':
        
        timeDirectory=Region.foamDictionary['controlDict']['startTime']
        
        
    elif Region.foamDictionary['controlDict']['startFrom']=='latestTime':
        timeDirectories=cfdGetTimeSteps(path,Region)
        timeDirectory=max(timeDirectories)
        
        
    elif Region.foamDictionary['controlDict']['startFrom']=='firstTime':   
        timeDirectory='0' 
        
    else:
        print("Error in controlDict: startFrom is not valid!")
        

    caseDirectoryPath = Region.caseDirectoryPath
    
    for root, directory,files in os.walk(caseDirectoryPath + "\\"+timeDirectory):
        if not files:
            print('Fields are not found in the %s directory' % (caseDirectoryPath + "\\"+timeDirectory+"!"))
    
    
    for file in files:
        
        fieldName=file
        fieldFilePath=caseDirectoryPath + "\\"+timeDirectory+"\\"+fieldName
        
        header=cfdGetFoamFileHeader(fieldFilePath)
        
        cfdSetupMeshField(Region,fieldName,header['class'])
        
        with open(fieldFilePath,"r") as fpid:
            contents=cfdReadCfdDictionary(fpid)
        
    return contents
    






                
















