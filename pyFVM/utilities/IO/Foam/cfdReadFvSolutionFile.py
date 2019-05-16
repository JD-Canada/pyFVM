
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadFvSolutionFile(caseDirectoryPath):
    
    print('Reading fvSolution file ...')
    
    fvSolutionFileDirectory = r"%s/system/fvSolution" % caseDirectoryPath 
    
    fvSolution={}
    
    with open(fvSolutionFileDirectory,"r") as fpid:
        
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue

            if "FoamFile" in tline:
                dictionary=cfdReadCfdDictionary(fpid)
                continue
           
            if "solvers" in tline:
                fvSolution['solvers']=cfdReadCfdDictionary(fpid)
                
                for key in fvSolution['solvers']:
                
                    if 'maxIter' in fvSolution['solvers'][key]:
                        continue
                    else:
                        fvSolution['solvers'][key]['maxIter']=20
                        continue

            if "SIMPLE" in tline:
                fvSolution['SIMPLE']=cfdReadCfdDictionary(fpid)
                continue

            if "relaxationFactors" in tline:
                fvSolution['relaxationFactors']=cfdReadCfdDictionary(fpid)
                continue
            
    return fvSolution

    