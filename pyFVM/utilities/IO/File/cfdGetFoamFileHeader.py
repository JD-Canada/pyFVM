from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdGetFoamFileHeader(fieldFilePath):

    with open(fieldFilePath,"r") as fpid:
        print('\nReading %s file ...' %(fieldFilePath))
       
        header={}
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue
            
            if "FoamFile" in tline:
                if not header:
                    header=cfdReadCfdDictionary(fpid)
                    return header
    
