import os
from pyFVM.src.time.cfdIsTimeDirectory import cfdIsTimeDirectory


def cfdGetTimeSteps(Region):
    
    """Finds valid time directories in case directory.
    
    Attributes:
        
       timeSteps (list): valid time steps.

    Returns:
        
       timeSteps
       
    Example usage:
        
        timeSteps = cfdGetTimeSteps(Region)
        
    """
    
    print("\n")
    print("Searching for time directories ... \n")

    timeSteps=[]
    for root, directory,files in os.walk(Region.caseDirectoryPath):
        
        for folder in directory:
            if cfdIsTimeDirectory(os.path.join(root, folder),Region):
                timeSteps.append(float(folder))
    print("\n")
    return timeSteps
        

