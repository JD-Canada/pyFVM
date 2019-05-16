import os

from pyFVM.src.fields.cfdGetFields import cfdGetFields


def cfdIsTimeDirectory(theDirectoryPath,Region):
    
    root, basename=os.path.split(theDirectoryPath)
    
    try:
        #throw ValueError
        check=float(basename)
        
        #else
        fields = cfdGetFields(Region)
        for file in os.listdir(theDirectoryPath):
            if str(file) in fields:
                print("%s is a time directory" % theDirectoryPath)
                return True
        
    except ValueError:
        print('%s is not a time directory, skipping ...' % theDirectoryPath)
        return False


