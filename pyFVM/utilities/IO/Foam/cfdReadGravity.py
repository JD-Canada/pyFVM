from pyFVM.utilities.IO.File.cfdReadAllDictionaries import cfdReadAllDictionaries

def cfdReadGravity(Region):

    gravityFilePath=Region.caseDirectoryPath + "/constant/g"
    
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