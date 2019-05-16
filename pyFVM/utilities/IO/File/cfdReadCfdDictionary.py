from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments

def cfdReadCfdDictionary(fpid,**kwargs):
    
    subDictionary=False
    dictionary={}
    
    if 'line' in kwargs:
        dictionary[kwargs.get("line")[0]]=kwargs.get("line")[1]
        
    for line, tline in enumerate(fpid):
        
        if not cfdSkipEmptyLines(tline):
            continue
        if not cfdSkipMacroComments(tline):
            continue            
        
        if "{" in tline:
            continue

        #check for end of subDictionary
        if "}" in tline and subDictionary == True:
            subDictionary = False
            continue
        
        if "}" in tline and subDictionary == False:
            break
            
        
        tline = tline.replace(";", "")
        
        if len(tline.split()) == 1 and subDictionary == False:
            subDictionary=True
            dictionary[tline.split()[0]]={}
            currentSubDictKey=tline.split()[0]
            continue
        
        
        if subDictionary == True:
            try:
                dictionary[currentSubDictKey][tline.split()[0]]=float(tline.split()[1])

            except ValueError:

                dictionary[currentSubDictKey][tline.split()[0]]=tline.split()[1]        
            continue
        else:
            try:
                dictionary[tline.split()[0]]=float(tline.split()[1])
            except ValueError:
                dictionary[tline.split()[0]]=tline.split()[1]
    return dictionary