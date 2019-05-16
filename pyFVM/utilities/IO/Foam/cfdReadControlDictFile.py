from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary


def cfdReadControlDictFile(caseDirectoryPath):
    print('Reading controlDict file ...')
    

    controlDictFileDirectory = r"%s/system/controlDict" % caseDirectoryPath
    
    try:
        with open(controlDictFileDirectory,"r") as fpid:
            controlDict={}
            for linecount, tline in enumerate(fpid):
                
                if not cfdSkipEmptyLines(tline):
                    continue
                
                if not cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=cfdReadCfdDictionary(fpid)
                    continue
    
                if len(tline.split()) > 1:
                    
                    controlDict=cfdReadCfdDictionary(fpid,line=tline.split())
                    
            return controlDict
                
    except FileNotFoundError:
        print('"controlDict" file is not found!!!' )
