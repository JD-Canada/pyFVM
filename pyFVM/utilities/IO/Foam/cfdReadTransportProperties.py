import os
from pyFVM.src.fields.cfdGetMeshField import cfdGetMeshField
from pyFVM.src.fields.cfdSetMeshField import cfdSetMeshField
from pyFVM.src.fields.cfdUpdateScale import cfdUpdateScale
from pyFVM.utilities.IO.File.cfdReadAllDictionaries import cfdReadAllDictionaries

def cfdReadTransportProperties(Region):
    """Reads the transportProperties dictionary 
       and sets the transportProperties in Region.fluid

       If rho, mu and Cp dictionaries are not user defined, creates them with default air properties
       Same for k (thermal conductivity) if the DT dictionary is present


    Attributes:
        
       Region (instance of cfdSetupRegion): the cfd Region.
       
    Example usage:
        
        cfdReadTransportProperties(Region)
        
    TODO:
       
       . 
    """ 



    
    transportPropertiesFilePath=Region.caseDirectoryPath+"/constant/transportProperties"
    
    
    if not os.path.isfile(transportPropertiesFilePath):
        pass
    
    else:
        print('Reading transport properties ...')
        
        transportDicts=cfdReadAllDictionaries(transportPropertiesFilePath)
        transportKeys=list(transportDicts)   
        
        Region.foamDictionary['transportProperties']={}
        
        for iKey in transportKeys:
            if iKey=='FoamFile' or iKey=='cfdTransportModel':
                pass
            elif not len(transportDicts[iKey])==8:
                print('FATAL: There is a problem with entry %s in transportProperties' %iKey )
                break
            else:
     
                theMeshField={}
                dimVector=[]
                boundaryPatch={} 
                Region.foamDictionary['transportProperties'][iKey]={}
                
                for iDim in transportDicts[iKey][0:7]:
                    dimVector.append(float(iDim))
    
                keyValue = float(transportDicts[iKey][7])
                
                theInteriorArraySize = Region.mesh['numberOfElements']
                theBoundaryArraySize = Region.mesh['numberOfBElements']
    
                theMeshField['phi']= [[keyValue] for i in range(theInteriorArraySize+theBoundaryArraySize)] 
                theMeshField['name']=iKey
                theMeshField['type']='volScalarField'
                theMeshField['dimensions']=transportDicts[iKey][0:7]
                theMeshField['prevIter']={}
                theMeshField['prevIter']['phi']=theMeshField['phi']   
                theMeshField['prevTimeStep']={}
                theMeshField['prevTimeStep']['phi']=theMeshField['phi']
          
                numberOfBPatches=int(Region.mesh['numberOfBoundaryPatches'])
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = keyValue;
                    boundaryPatch['type'] = 'zeroGradient';
                    theMeshField['boundaryPatch'] = boundaryPatch;
        
                cfdSetMeshField(Region,theMeshField)
                
                Region.foamDictionary['transportProperties'][iKey]['name']=iKey
                Region.foamDictionary['transportProperties'][iKey]['propertyValue']=keyValue
                Region.foamDictionary['transportProperties'][iKey]['dimensions']=transportDicts[iKey][0:7]
    
                cfdUpdateScale(Region,iKey)
                
        if not 'rho' in transportKeys:
            theMeshField={}
            dimVector=[]
            boundaryPatch={} 
                        
            theInteriorArraySize = Region.mesh['numberOfElements']
            theBoundaryArraySize = Region.mesh['numberOfBElements']
    
            theMeshField['phi']= [[1.] for i in range(theInteriorArraySize+theBoundaryArraySize)] 
            theMeshField['name']='rho'
            theMeshField['type']='volScalarField'
            theMeshField['dimensions']=['0', '0', '0', '0', '0', '0', '0'] #['1', '-3', '0', '0', '0', '0', '0']
            theMeshField['prevIter']={}
            theMeshField['prevIter']['phi']=theMeshField['phi']   
            theMeshField['prevTimeStep']={}
            theMeshField['prevTimeStep']['phi']=theMeshField['phi']
      
            numberOfBPatches=int(Region.mesh['numberOfBoundaryPatches'])
            for iPatch in range(0,numberOfBPatches):
                boundaryPatch['value'] = 1;
                boundaryPatch['type'] = 'zeroGradient';
                theMeshField['boundaryPatch'] = boundaryPatch;
    
            cfdSetMeshField(Region,theMeshField)
            
            cfdUpdateScale(Region,'rho')
                 
        Region.compressible='false' 
    
        if not 'mu' in transportKeys:
            theMeshField={}
            dimVector=[]
            boundaryPatch={} 
                        
            theInteriorArraySize = Region.mesh['numberOfElements']
            theBoundaryArraySize = Region.mesh['numberOfBElements']
    
            theMeshField['phi']= [[1E-3] for i in range(theInteriorArraySize+theBoundaryArraySize)] 
            theMeshField['name']='mu'
            theMeshField['type']='volScalarField'
            theMeshField['dimensions']=['0', '0', '0', '0', '0', '0', '0'] #['1', '-3', '0', '0', '0', '0', '0']
            theMeshField['prevIter']={}
            theMeshField['prevIter']['phi']=theMeshField['phi']   
            theMeshField['prevTimeStep']={}
            theMeshField['prevTimeStep']['phi']=theMeshField['phi']
      
            numberOfBPatches=int(Region.mesh['numberOfBoundaryPatches'])
            for iPatch in range(0,numberOfBPatches):
                boundaryPatch['value'] = 1E-3;
                boundaryPatch['type'] = 'zeroGradient';
                theMeshField['boundaryPatch'] = boundaryPatch;
    
            cfdSetMeshField(Region,theMeshField)
                 
        if not 'Cp' in transportKeys:
            theMeshField={}
            dimVector=[]
            boundaryPatch={} 
                        
            theInteriorArraySize = Region.mesh['numberOfElements']
            theBoundaryArraySize = Region.mesh['numberOfBElements']
    
            theMeshField['phi']= [[1004.] for i in range(theInteriorArraySize+theBoundaryArraySize)] 
            theMeshField['name']='Cp'
            theMeshField['type']='volScalarField'
            theMeshField['dimensions']=['0', '0', '0', '0', '0', '0', '0'] #['1', '-3', '0', '0', '0', '0', '0']
            theMeshField['prevIter']={}
            theMeshField['prevIter']['phi']=theMeshField['phi']   
            theMeshField['prevTimeStep']={}
            theMeshField['prevTimeStep']['phi']=theMeshField['phi']
      
            numberOfBPatches=int(Region.mesh['numberOfBoundaryPatches'])
            for iPatch in range(0,numberOfBPatches):
                boundaryPatch['value'] = 1004.;
                boundaryPatch['type'] = 'zeroGradient';
                theMeshField['boundaryPatch'] = boundaryPatch;
    
            cfdSetMeshField(Region,theMeshField)
    
        if not 'k' in transportKeys:
            if 'DT' in transportKeys:
                theMeshField={}
                dimVector=[]
                boundaryPatch={} 
                kField=[]
                theInteriorArraySize = Region.mesh['numberOfElements']
                theBoundaryArraySize = Region.mesh['numberOfBElements']
    
                DTField = cfdGetMeshField(Region,'DT')['phi']
                CpField = cfdGetMeshField(Region,'Cp')['phi']
                rhoField = cfdGetMeshField(Region,'rho')['phi']
    
                
                for i in range(0,len(DTField)):            
                    kField.append([DTField[i][0]*CpField[i][0]*rhoField[i][0]])                    
    
                theMeshField['phi']= kField
                theMeshField['name']='k'
                theMeshField['type']='volScalarField'
                theMeshField['dimensions']=['0', '0', '0', '0', '0', '0', '0'] #['1', '-3', '0', '0', '0', '0', '0']
                theMeshField['prevIter']={}
                theMeshField['prevIter']['phi']=theMeshField['phi']   
                theMeshField['prevTimeStep']={}
                theMeshField['prevTimeStep']['phi']=theMeshField['phi']
          
                numberOfBPatches=int(Region.mesh['numberOfBoundaryPatches'])
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = kField[0];
                    boundaryPatch['type'] = 'zeroGradient';
                    theMeshField['boundaryPatch'] = boundaryPatch;
        
                cfdSetMeshField(Region,theMeshField)