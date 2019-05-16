
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadFvSchemesFile(caseDirectoryPath):
    
    print('Reading fvSchemes file ...')
    
    fvSchemesFileDirectory = r"%s/system/fvSchemes" % caseDirectoryPath 
    
    fvSchemes={}
    
    with open(fvSchemesFileDirectory,"r") as fpid:
        
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue
            
            if "FoamFile" in tline:
                dictionary=cfdReadCfdDictionary(fpid)
                continue

            if "ddtSchemes" in tline:
                fvSchemes['ddtSchemes']=cfdReadCfdDictionary(fpid)
                continue

            if "gradSchemes" in tline:
                fvSchemes['gradSchemes']=cfdReadCfdDictionary(fpid)
                continue
            
            if "divSchemes" in tline:
                fvSchemes['divSchemes']=cfdReadCfdDictionary(fpid)
                continue
            
            if "laplacianSchemes" in tline:
                fvSchemes['laplacianSchemes']=cfdReadCfdDictionary(fpid)
                continue         
            
            if "interpolationSchemes" in tline:
                fvSchemes['interpolationSchemes']=cfdReadCfdDictionary(fpid)
                continue      
            
            if "snGradSchemes" in tline:
                fvSchemes['snGradSchemes']=cfdReadCfdDictionary(fpid)
                continue      
            
            if "fluxRequired" in tline:
                fvSchemes['fluxRequired']=cfdReadCfdDictionary(fpid)
                continue            

    return fvSchemes

    