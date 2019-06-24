import os
from pyFVM.utilities.IO.File.cfdReadAllDictionaries import cfdReadAllDictionaries

def cfdReadGravity(Region):

    """Read the g file in the constant directory
    and returns the gravity vector and dimensions. 


    Attributes:
        
       Region (str): the cfd Region.
       
    Example usage:
        
        cfdReadGravity(Region)
        
    TODO:
       
       . 
    """    
    
    gravityFilePath=Region.caseDirectoryPath + "/constant/g"
    
    if not os.path.isfile(gravityFilePath):
        print('\n\nNo g file found\n')
        pass
    
    else:
        print('\n\nReading Gravity ...\n')        
        gravityDict = cfdReadAllDictionaries(gravityFilePath)
        
        dimensions=[]
        for iEntry in gravityDict['dimensions']:
            
            try:
                dimensions.append(float(iEntry))
            except ValueError:
                pass
        
        value=[]
        for iEntry in gravityDict['value']:
        
            iEntry=iEntry.replace("(","")
            iEntry=iEntry.replace(")","")
            
            try:
                value.append(float(iEntry))
            except ValueError:
                pass
        
        Region.foamDictionary['g']={}
        
        Region.foamDictionary['g']['dimensions']=dimensions
        Region.foamDictionary['g']['value']=value