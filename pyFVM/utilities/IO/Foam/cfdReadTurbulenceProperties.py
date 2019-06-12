from pyFVM.utilities.IO.File.cfdReadAllDictionaries import cfdReadAllDictionaries

def cfdReadTurbulenceProperties(Region):
 
    """Reads the turbulenceProperties dictionary 
        and sets the turbulence properties in Regio.foamDictionary
        If there is no turbulenceProperties file, sets the turbulence
        model to 'laminar'    


    Attributes:
        
       Region (str): the cfd Region.
       
    Example usage:
        
        cfdReadTurbulenceProperties(Region)
        
    TODO:
       
       . 
    """   

    Region.foamDictionary['turbulenceProperties']={}
    
    turbulencePropertiesFilePath=Region.caseDirectoryPath+"/constant/turbulenceProperties"
    
    if not turbulencePropertiesFilePath:
        print('Hola')
        Region.foamDictionary['turbulenceProperties']['turbulence'] = 'off'
        Region.foamDictionary['turbulenceProperties']['RASModel'] = 'laminar'
    
    else:
        print('\n\nReading Turbulence Properties ...\n')
        
        turbulencePropertiesDict = cfdReadAllDictionaries(turbulencePropertiesFilePath)
    
        turbulenceKeys = turbulencePropertiesDict.keys();
        
        for iDict in turbulenceKeys:
            if 'FoamFile' in iDict or 'simulationType' in iDict: 
                pass
            else:
                for iSubDict in turbulencePropertiesDict[iDict]:
                    Region.foamDictionary['turbulenceProperties'][iSubDict]=turbulencePropertiesDict[iDict][iSubDict][0]