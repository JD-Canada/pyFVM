import os

class cfdSetupRegion():

    """Sets up the simulation's 'Region'.

    An instance of the cfdSetupRegion class is required for the case to run. 
    The instance is created at the beginning of each case.

    Attributes:
        
       caseDirectoryPath (str): path to directory from which the script is run.
       
       STEAD_STATE_RUN (bool): steady state (True), transient (False)
       
       foamDictionary (dict): container for 'mesh' and other subdictionaries.
       
       fluid (dict): container for fluid properties.

    Example usage:
        Region = cfdSetupRegion()
        

    Region is now an instance of the cfdSetupRegion class.
    
    TODO:
        Add details about attributes as code grows in complexity.

    """

    def __init__(self):
        
        """Initiates the class instance with the caseDirectoryPath attribute 
        and adds the 'foamDictionary' and 'fluid' dictionaries. Reminder - 
        __init__ functions are run automatically when a new class instance is 
        created. This docstring does not appear in Sphinx documentation.
    
        """

        self.caseDirectoryPath = os.getcwd()
        
        self.STEADY_STATE_RUN = True
        
        self.foamDictionary={}
        
        self.fluid={}
        
        print('Working case directory is %s' % self.caseDirectoryPath)

