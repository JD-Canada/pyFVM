import pandas as pd
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadOwnerFile(ownerFile):
    with open(ownerFile,"r") as fpid:
        print('Reading owner file ...')
        owners=[]
        start=False
        
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue
            
            if "FoamFile" in tline:
                dictionary=cfdReadCfdDictionary(fpid)
                continue

            if len(tline.split()) ==1:
               
                #load and skip number of owners
                if not start:
                    nbrOwner=tline
                    start=True
                    continue

                if "(" in tline:
                    continue
                if ")" in tline:
                    break
                else:
                    owners.append(int(tline.split()[0]))
                   
            
            

    return owners

    