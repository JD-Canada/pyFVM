import os

def cfdPrintMainHeader():
    
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-* pyFVM *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n');
    print('|| A python finite volume code based heavily on the uFVM code written in the Matlab language. ||\n');
    print('|| uFVM was written by the CFD Group at the American University of Beirut.   ||\n');
    print('|| This is an academic CFD package developed for learning purposes to serve ||\n');
    print('|| the student community.                                           ||\n');
    print('----------------------------------------------------------------------\n');
    print(' Credits:\n \tMarwan Darwish, Mhamad Mahdi Alloush for uFVM code\n');
    print('\tcfd@aub.edu.lb\n');
    print('\tAmerican University of Beirut\n');
    print('\tuFVM v1.5, 2018\n');
    
    print(' Python version credits:\n Sergio Croquez and Jason Duguay for Python translation\n');
    print(' Both authors are postdocs at the Université de Sherbrooke\n');
    print(' Québec, Canada');

    print('\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n\n');


def cfdGetFoamFileHeader(fieldFilePath):

    with open(fieldFilePath,"r") as fpid:
        print('Reading %s file ...' %(fieldFilePath))
       
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

def cfdSkipEmptyLines(tline):

    if not tline.strip():
        tline = False
    else:
        tline = tline
    return tline    

def cfdSkipMacroComments(tline):

    trimmedTline = tline.strip()
    
    if "/*" in trimmedTline:
        tline = False
    elif "|" in trimmedTline:
        tline = False
    elif "\*" in trimmedTline:
        tline = False
    elif "*" in trimmedTline: 
        tline = False
    else:
        tline = tline
    return tline

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

def cfdReadAllDictionaries(filePath):
    
    """Returns all dictionary entries inside an OpenFOAM file. 
    
    This function does not directly mimic any function in uFVM. It was added to 
    make accessing a file's dictionary keywords and associated values easily
    within one function. The user can then extract the 'raw' values by 
    navigating the returned dictionary.
    

    Attributes:
        
       filePath (str): path to file to read.
       
    Example usage:
        
        Region = cfdReadAllDictionaries(filePath)
        
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


def cfdGetKeyValue(key, valueType, fileID):

    """Returns the value of the 'key' entry in an OpenFOAM file.
    
    
    
    Attributes:
        
       key (str): keyword to look for in line.
       valueType (str):
       fileID (str): path to initial file to look through.
       
    Example usage:
        
        values = cfdGetKeyValue(key, valueType, fileID)
        
    TODO:
        Add functionality for valueTypes 'scalar', 'cfdLabelList' and
        'cfdScalarList'. We can add these as we encounter a need for them. 
    """
    
    with open(fileID,"r") as fpid:

        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if key in tline:
                
                tline=tline.replace(";","")
                tline=tline.replace("[","")
                tline=tline.replace("]","")
                tline=tline.replace("(","")
                tline=tline.replace(")","")

                splittedTline=tline.split()
                #splittedTline.remove(key)
                
#                print(splittedTline)
                
                if 'uniform' in splittedTline:
                    
                    distribution='uniform'
                    
                elif 'nonuniform' in splittedTline:
                    distribution='nonuniform'
                    
                else:
                    distribution = None
                    
                value=[]
                    
                for iEntry in splittedTline:
                    
                    try:
                        value.append(float(iEntry))
                    except ValueError:
                        pass
                        
    return [key, distribution, value]


def cfdReadUniformVolVectorFieldValue(volVectorFieldEntry):

    """Returns [u,v,w] type list from a 'value uniform (u v w)' dictionary entry. 
    
    Basically strips off '(' and ')' and returns a python list object, e.g. 
    [0, 1.2, 5]
    
    Attributes:
        
       volVectorFieldEntry (list): list containing ['uniform', '(u', 'v','w)']
       
    Example usage:
        
        Region = cfdReadUniformVolVectorFieldValue(volVectorFieldEntry)
        
    """    
    
    vector=[]
    
    for item in volVectorFieldEntry:
        
        if item == 'uniform':
            uniform='uniform'
            continue
    
        item=item.replace("(","")
        item=item.replace(")","")
        
        vector.append(float(item))
        
    return uniform, vector

