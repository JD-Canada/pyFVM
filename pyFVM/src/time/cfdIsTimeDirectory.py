import os

from pyFVM.src.fields.cfdGetFields import cfdGetFields


def cfdIsTimeDirectory(theDirectoryPath,Region):

    """Checks input directory if it is a valid time directory.
    
    Attributes:
        
       timeSteps (list): valid time steps.

    Returns:
        
       boolean
       
    Example usage:
        
        timeSteps = cfdIsTimeDirectory(theDirectoryPath,Region)
        
    """
    
    root, basename=os.path.split(theDirectoryPath)
    
    try:
        #if string, throw ValueError
        check=float(basename)
        
        #else
        fields = cfdGetFields(Region)
        
        for file in os.listdir(theDirectoryPath):
            
            #check if file name is a field
            if str(file) in fields:
                
                print("%s is a time directory" % theDirectoryPath)
                
                return True
        
    except ValueError:
        
        print('%s is not a time directory, skipping ...' % theDirectoryPath)
        
        return False


