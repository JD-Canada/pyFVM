
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadBoundaryFile(boundaryFile):
    with open(boundaryFile,"r") as fpid:
        print('Reading boundary file ...')
       
        boundaries={}
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue
            
            if "FoamFile" in tline:
                dictionary=cfdReadCfdDictionary(fpid)
                continue

            if len(tline.split()) ==1:
                if "(" in tline:
                    continue
                if ")" in tline:
                    continue
                
                if tline.strip().isdigit():
                    
                    numberOfBoundaries = tline.split()[0]
                    continue
               
                boundaries[tline.split()[0]]=cfdReadCfdDictionary(fpid)
            
            if len(tline.split()) > 1:
                
                boundaries=cfdReadCfdDictionary(fpid,line=tline.split())
                
    return boundaries, numberOfBoundaries

    