import pandas as pd
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadNeighbourFile(neighbourFile):
    with open(neighbourFile,"r") as fpid:
        print('Reading neighbour file ...')
        neighbours=[]
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
                    numberOfNeighbours=int(tline)
                    start=True
                    continue

                if "(" in tline:
                    continue
                if ")" in tline:
                    break
                else:
                    neighbours.append(int(tline.split()[0]))
                   

    return  numberOfNeighbours,neighbours

    