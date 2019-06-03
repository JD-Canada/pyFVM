from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines



def cfdGetKeyValue(key, valueType, fileID):

    """Returns the value of the 'key' entry in an OpenFOAM file.
    
    
    
    Attributes:
        
       key (str): keyword to look for in line.
       valueType (str): list of time directories in case.
       fileID (str): path to initial file to look through.
       
    Example usage:
        
        Region = cfdGetKeyValue(key, valueType, fileID)
        
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
                
                print(splittedTline)
                
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
                
                