import pandas as pd
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary

def cfdReadFacesFile(facesFile):
    with open(facesFile,"r") as fpid:
        print('Reading faces file ...')
        faceNodes=[]
        
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
                else:
                    
                    numberOfFaces = int(tline.split()[0])
                    continue
            
            tline=tline.replace("("," ")
            tline=tline.replace(")","")
            faceNodesi=[]
            for count, node in enumerate(tline.split()):
                if count == 0:
                    continue
                    #faceNodesi.append(int(node))
                else:
                    faceNodesi.append(float(node))
            
            faceNodes.append(faceNodesi)

    return faceNodes, numberOfFaces

    