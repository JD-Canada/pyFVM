import os

from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments

def cfdReadAllDictionaries(filePath):
    
    """Returns all dictionary entries inside a OpenFOAM file. 
    
    This function does not directly mimic any function in uFVM. It was added to 
    make accessing a file's dictionary keywords and associated values easily
    within one function. The user can then extract the 'raw' values by 
    navigating the returned dictionary.
    

    Attributes:
        
       filePath (str): path to file to read.
       
    Example usage:
        
        Region = cfdReadAllDictionaries(filePath)
        
    TODO:
        Add functionality for valueTypes 'scalar', 'cfdLabelList' and
        'cfdScalarList'. We can add these as we encounter a need for them. 
    """    
    try:
        with open(filePath,"r") as fpid:
        
            isDictionary=False
            isSubDictionary=False
            dictionaries={}
            
            for line, tline in enumerate(fpid):
                
                
                if not cfdSkipEmptyLines(tline):
                    continue
                
                if not cfdSkipMacroComments(tline):
                    continue            
                
                if "{" in tline and isDictionary == False:
                    isDictionary=True
                    continue
        
                if "{" in tline and isDictionary == True:
                    isSubDictionary=True
                    continue
        
                if "}" in tline and isSubDictionary == True:
                    isSubDictionary = False
                    continue
        
                if "}" in tline and isDictionary == True:
                    isDictionary = False
                    continue
                
                tline = tline.replace(";", "")
        
                #read one line dictionaries elements (e.g. 'dimensions [0 1 -1 0 0 0 0]')
                if len(tline.split()) > 1 and isDictionary == False:
                    tline = tline.replace("[", "")
                    tline = tline.replace("]", "")
                    dictionaries[tline.split()[0]]=tline.split()[1:]
                    continue
                
                #read dictionaries    
                if len(tline.split()) == 1 and isDictionary == False:
                    
                    currentDictionaryName=tline.split()[0]
                    dictionaries[currentDictionaryName]={}
                    continue
        
                if len(tline.split()) == 1 and isDictionary == True:
                    
                    currentSubDictionaryName=tline.split()[0]
                    dictionaries[currentDictionaryName][currentSubDictionaryName]={}
                    continue
        
                if len(tline.split()) > 1 and isDictionary == True and isSubDictionary == False:
        
                    dictionaries[currentDictionaryName][tline.split()[0]]=tline.split()[1:]
                    continue
               
                if len(tline.split()) > 1 and isSubDictionary == True:
        
                    dictionaries[currentDictionaryName][currentSubDictionaryName][tline.split()[0]]=tline.split()[1:]
                    
                    continue     
            
            return dictionaries
        
    except FileNotFoundError:
            
        print('Warning: %s file is not found!!!' % os.path.split(filePath)[1])