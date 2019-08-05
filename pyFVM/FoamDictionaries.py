import os
import sys
import pyFVM.IO as io
import pyFVM.Field as field
import pyFVM.Math as mth
import numpy as np


class FoamDictionaries():
    
    def __init__(self, Region):
        
        self.Region=Region
        self.cfdReadControlDictFile()
        self.cfdReadFvSchemesFile()
        self.cfdReadFvSolutionFile()
        self.cfdReadGravity()
        self.cfdReadTurbulenceProperties()
        
        self.cfdGetFields()

        
    def cfdReadControlDictFile(self):
        print('Reading controlDict file ...')
        
        controlDictFileDirectory = r"%s/system/controlDict" % self.Region.caseDirectoryPath
        
        try:
            with open(controlDictFileDirectory,"r") as fpid:
                self.controlDict={}
                for linecount, tline in enumerate(fpid):
                    
                    if not io.cfdSkipEmptyLines(tline):
                        continue
                    
                    if not io.cfdSkipMacroComments(tline):
                        continue
                    
                    if "FoamFile" in tline:
                        dictionary=io.cfdReadCfdDictionary(fpid)
                        continue
        
                    if len(tline.split()) > 1:
                        
                        self.controlDict=io.cfdReadCfdDictionary(fpid,line=tline.split())
                        
        except FileNotFoundError:
            print('"controlDict" file is not found!!!' )


    def cfdReadFvSchemesFile(self):
        
        print('Reading fvSchemes file ...')
        
        fvSchemesFileDirectory = r"%s/system/fvSchemes" % self.Region.caseDirectoryPath 
        
        self.fvSchemes={}
        
        with open(fvSchemesFileDirectory,"r") as fpid:
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
                
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if "ddtSchemes" in tline:
                    self.fvSchemes['ddtSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if "gradSchemes" in tline:
                    self.fvSchemes['gradSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue
                
                if "divSchemes" in tline:
                    self.fvSchemes['divSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue
                
                if "laplacianSchemes" in tline:
                    self.fvSchemes['laplacianSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue         
                
                if "interpolationSchemes" in tline:
                    self.fvSchemes['interpolationSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue      
                
                if "snGradSchemes" in tline:
                    self.fvSchemes['snGradSchemes']=io.cfdReadCfdDictionary(fpid)
                    continue      
                
                if "fluxRequired" in tline:
                    self.fvSchemes['fluxRequired']=io.cfdReadCfdDictionary(fpid)
                    continue            
    
    def cfdReadFvSolutionFile(self):
        
        print('Reading fvSolution file ...')
        
        fvSolutionFileDirectory = r"%s/system/fvSolution" % self.Region.caseDirectoryPath 
        
        self.fvSolution={}
        
        with open(fvSolutionFileDirectory,"r") as fpid:
            
            for linecount, tline in enumerate(fpid):
                
                if not io.cfdSkipEmptyLines(tline):
                    continue
                
                if not io.cfdSkipMacroComments(tline):
                    continue
    
                if "FoamFile" in tline:
                    dictionary=io.cfdReadCfdDictionary(fpid)
                    continue
               
                if "solvers" in tline:
                    self.fvSolution['solvers']=io.cfdReadCfdDictionary(fpid)
                    
                    for key in self.fvSolution['solvers']:
                    
                        if 'maxIter' in self.fvSolution['solvers'][key]:
                            continue
                        else:
                            self.fvSolution['solvers'][key]['maxIter']=20
                            continue
    
                if "SIMPLE" in tline:
                    self.fvSolution['SIMPLE']=io.cfdReadCfdDictionary(fpid)
                    continue
    
                if "relaxationFactors" in tline:
                    self.fvSolution['relaxationFactors']=io.cfdReadCfdDictionary(fpid)
                    continue
                
    def cfdReadGravity(self):
    
        """Read the g file in the constant directory
        and returns the gravity vector and dimensions. 
        Attributes:
            
           Region (str): the cfd Region.
           
        Example usage:
            
            cfdReadGravity(Region)
            
        TODO:
           
           . 
        """    
        
        gravityFilePath=self.Region.caseDirectoryPath + "/constant/g"
        
        if not os.path.isfile(gravityFilePath):
            print('\n\nNo g file found\n')
            pass
        
        else:
            print('Reading Gravity file ...')        
            gravityDict = io.cfdReadAllDictionaries(gravityFilePath)
            
            dimensions=[]
            for iEntry in gravityDict['dimensions']:
                
                try:
                    dimensions.append(float(iEntry))
                except ValueError:
                    pass
            
            value=[]
            for iEntry in gravityDict['value']:
            
                iEntry=iEntry.replace("(","")
                iEntry=iEntry.replace(")","")
                
                try:
                    value.append(float(iEntry))
                except ValueError:
                    pass
            
            self.g={}
            self.g['dimensions']=dimensions
            self.g['value']=value

    def cfdReadTurbulenceProperties(self):
     
        """Reads the turbulenceProperties dictionary 
           and sets the turbulence properties in Region.foamDictionary
           If there is no turbulenceProperties file, sets the turbulence
           model to 'laminar'.   
    
    
        Attributes:
            
           Region (instance of cfdSetupRegion): the cfd Region.
           
        Example usage:
            
            cfdReadTurbulenceProperties(Region)
            
        """   
    
        self.turbulenceProperties={}
        
        turbulencePropertiesFilePath=self.Region.caseDirectoryPath+"/constant/turbulenceProperties"
        
        if not turbulencePropertiesFilePath:
            self.turbulenceProperties['turbulence'] = 'off'
            self.turbulenceProperties['RASModel'] = 'laminar'
        
        else:
            print('Reading Turbulence Properties ...')
            
            turbulencePropertiesDict = io.cfdReadAllDictionaries(turbulencePropertiesFilePath)
        
            turbulenceKeys = turbulencePropertiesDict.keys();
            
            for iDict in turbulenceKeys:
                if 'FoamFile' in iDict or 'simulationType' in iDict: 
                    pass
                else:
                    for iSubDict in turbulencePropertiesDict[iDict]:
                        self.turbulenceProperties[iSubDict]=turbulencePropertiesDict[iDict][iSubDict][0]


    def cfdGetTimeSteps(self):
        
        """Finds valid time directories in case directory.
        
        Attributes:
            
           timeSteps (list): valid time steps.
    
        Returns:
            
           timeSteps
           
        Example usage:
            
            timeSteps = cfdGetTimeSteps(Region)
            
        """
        
        print("Searching for time directories ... \n")
    
        self.Region.timeSteps=[]
        for root, directory,files in os.walk(self.Region.caseDirectoryPath):
            
            for folder in directory:
                if self.cfdIsTimeDirectory(os.path.join(root, folder)):
                    
                    #check for decimal place in folder name
                    if float(folder)-int(folder) != 0:
                        self.Region.timeSteps.append(str(float(folder)))
                    elif float(folder)-int(folder) ==0:
                        self.Region.timeSteps.append(str(int(folder)))

        print("\n")
        

    def cfdIsTimeDirectory(self,theDirectoryPath):
    
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

            for file in os.listdir(theDirectoryPath):
                
                #check if file name is a field
                if str(file) in self.Region.fields:
                    
                    print("%s is a time directory" % theDirectoryPath)
                    
                    return True
            
        except ValueError:
            
            print('%s is not a time directory, skipping ...' % theDirectoryPath)
            
            return False

    def cfdGetFields(self):
        
        """Gets field names from keys contained in Region.foamDictionary['fvSolution'].
        
        Attributes:
            
           fields (list): fields.
    
        """
        
        self.Region.fields=[]
        
        for key in self.fvSolution['solvers']:
    
            self.Region.fields.append(key)
            
                        
    def cfdReadTimeDirectory(self):                    
        
        
        #manua
        kwargs=[]
        
        if len(kwargs) > 0:
            self.Region.timeDirectory=kwargs['time']
            
        elif self.controlDict['startFrom']=='startTime':
            self.Region.timeDirectory=str(int(self.controlDict['startTime']))
            
            
        elif self.controlDict['startFrom']=='latestTime':
            self.cfdGetTimeSteps()
            self.Region.timeDirectory=max(self.Region.timeSteps)
            
        elif self.controlDict['startFrom']=='firstTime':   
            ## I think in this case, the timeDirectory should be the minimum in 
            ## the list of time directories in the working folder (analogous to
            ## the latestTime case)
            self.cfdGetTimeSteps()
            self.Region.timeDirectory=min(self.Region.timeSteps)         
            # self.Region.timeDirectory='0' 
            
        else:
            print("Error in controlDict: startFrom is not valid!")
        
        for root, directory,files in os.walk(self.Region.caseDirectoryPath + os.sep +str(self.Region.timeDirectory)):

            if not files:
                print('Fields are not found in the %s directory' % (self.Region.caseDirectoryPath + os.sep +self.Region.timeDirectory+"!"))

        theNumberOfInteriorFaces = self.Region.mesh.numberOfInteriorFaces
        theNumberOfElements = self.Region.mesh.numberOfElements                       
                        
        for file in files:
            
            fieldName=file
            
            fieldFilePath=self.Region.caseDirectoryPath + os.sep +self.Region.timeDirectory+os.sep +fieldName
            
            header=io.cfdGetFoamFileHeader(fieldFilePath)
            
            self.Region.fluid[fieldName]=field.Field(self.Region,fieldName,header['class']) 

            self.Region.fluid[fieldName].dimensions=io.cfdGetKeyValue('dimensions','dimensions',fieldFilePath)[2]                       
                        
            internalField = io.cfdGetKeyValue('internalField','string',fieldFilePath)
            
            valueType=internalField[1]
            
            if self.Region.fluid[fieldName].type=='surfaceScalarField':
                
                print('surfaceScalarFields are not yet handled.')
                
            else:
                
                #reads and sets either volScalarField or volVectorField
        
                if valueType == 'uniform':
                    
                    if self.Region.fluid[fieldName].type=='volScalarField':
                        
                        value_str = internalField[2][0]
                        for count, subList in enumerate(self.Region.fluid[fieldName].phi):
                            if count > theNumberOfElements-1:
                                continue
                            else:
                                subList[0]=value_str
                            
                    elif self.Region.fluid[fieldName].type=='volVectorField':
                        
                        value_str = internalField[2]
                        for count, subList in enumerate(self.Region.fluid[fieldName].phi):
                            if count > theNumberOfElements-1:
                                continue
                            else:
                                
                                self.Region.fluid[fieldName].phi[count]=list(value_str)                                    
                        
                elif valueType == 'nonuniform':
                    print('The function cfdReadNonuniformList() is not yet writen.')                        
                        
#                theNumberOfBPatches = len(self.Region.mesh.cfdBoundaryPatchesArray)
                        
                for iBPatch, values in self.Region.mesh.cfdBoundaryPatchesArray.items():
                    
                    numberOfBFaces=values['numberOfBFaces']
                    iFaceStart=values['startFaceIndex']
                    
                    iElementStart = self.Region.mesh.numberOfElements + iFaceStart - self.Region.mesh.numberOfInteriorFaces 
                    iElementEnd = iElementStart+numberOfBFaces-1
                    
                    boundaryFile = io.cfdReadAllDictionaries(fieldFilePath)
                    boundaryType = boundaryFile['boundaryField'][iBPatch]['type'][0] 
        
                    try:
                        boundaryValue = boundaryFile['boundaryField'][iBPatch]['value']
                        valueType, boundaryValue = io.cfdReadUniformVolVectorFieldValue(boundaryValue)
                        
                    except KeyError:
                        
                        if boundaryType == 'zeroGradient' or boundaryType == 'empty' : 
                            
                            if self.Region.fluid[fieldName].type=='volScalarField' or self.Region.fluid[fieldName].type=='surfaceScalarField':
                                
                                boundaryValue = 0                        
                            elif self.Region.fluid[fieldName].type=='volVectorField':
                                
                                boundaryValue = [0,0,0]  
                                
                        else:
                            print('Warning: The %s field\'s %s boundary does not have a \'value\' entry' %(fieldName, iBPatch))
                            
                    except ValueError:                
                            print("Error: Oops, code cannot yet handle nonuniform boundary conditions")
                            print("       Not continuing any further ... apply uniform b.c.'s to continue")
                            break               
        
                    try:
                       
                        if valueType == 'uniform':
                            
                            if self.Region.fluid[fieldName].type=='volScalarField' or self.Region.fluid[fieldName].type=='surfaceScalarField':
            
                                for count, subList in enumerate(self.Region.fluid[fieldName].phi):
                                    if count < iElementStart or count > iElementEnd:
                                        continue
                                    else:
                                        self.Region.fluid[fieldName].phi[count]=boundaryValue
                                        
                            if self.Region.fluid[fieldName].type=='volVectorField':
                                
                                for count, subList in enumerate(self.Region.fluid[fieldName].phi):
                                    
                                    if count < iElementStart or count > iElementEnd:
                                        
                                        continue
                                    else:
                                        #print(count)
                                        #print(boundaryValue)
                                        self.Region.fluid[fieldName].phi[count]=boundaryValue
                        
                    except NameError:
                        
                        self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]={}
                        self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]['type']=boundaryType
                        del(boundaryType)
                        continue
                    
                    self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]={}
                    self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]['type']=boundaryType
                    self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]['valueType']=valueType
                    self.Region.fluid[fieldName].boundaryPatchRef[iBPatch]['value']=boundaryValue

                    del(boundaryValue)
                    del(valueType)
                    del(boundaryType)                       
                        
                        
                        
    def cfdReadTransportProperties(self):
        
        """Reads the transportProperties dictionary and sets the 
           transportProperties in Region.fluid If rho, mu and Cp dictionaries 
           are not user defined, creates them with default air properties
           Same for k (thermal conductivity) if the DT dictionary is present
           
        Attributes:
            
           Region (instance of cfdSetupRegion): the cfd Region.
           
        Example usage:
            
            cfdReadTransportProperties(Region)
            
        """ 
    
        transportPropertiesFilePath=self.Region.caseDirectoryPath+"/constant/transportProperties"
                        
        if not os.path.isfile(transportPropertiesFilePath):
            pass
    
        else:
            print('\nReading transport properties ...')
    
            transportDicts=io.cfdReadAllDictionaries(transportPropertiesFilePath)
            transportKeys=list(transportDicts)   
    
            self.transportProperties={}
    
            for iKey in transportKeys:
                     
                if iKey=='FoamFile' or iKey=='cfdTransportModel':
                    pass
                
                elif not len(transportDicts[iKey])==8:
                    #not sure what this does
                    print('FATAL: There is a problem with entry %s in transportProperties' %iKey )
                    break
                else:
    
                    dimVector=[]
                    boundaryPatch={} 
                    self.transportProperties[iKey]={}
    
                    for iDim in transportDicts[iKey][0:7]:
                        dimVector.append(float(iDim))
    
                    keyValue = float(transportDicts[iKey][7])
    
                    self.Region.fluid[iKey]=field.Field(self.Region,iKey,'volScalarField')
                    self.Region.fluid[iKey].dimensions=transportDicts[iKey][0:7]  
                    self.Region.fluid[iKey].phi.fill(keyValue)
            
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                    for iPatch in range(0,numberOfBPatches):
                        
                        boundaryPatch['value'] = keyValue
                        boundaryPatch['type'] = 'zeroGradient'
                        self.Region.fluid[iKey].boundaryPatch = boundaryPatch

                    self.transportProperties[iKey]['name']=iKey
                    self.transportProperties[iKey]['propertyValue']=keyValue
                    self.transportProperties[iKey]['dimensions']=transportDicts[iKey][0:7]

                    self.Region.fluid[iKey].cfdUpdateScale()
    
            if not 'rho' in transportKeys:
                
                boundaryPatch={} 
    
                self.Region.fluid['rho']=field.Field(self.Region,'rho','volScalarField')
                self.Region.fluid['rho'].dimensions=[0., 0., 0., 0., 0., 0.,0.]
                self.Region.fluid['rho'].phi.fill(1.)

                numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = 1;
                    boundaryPatch['type'] = 'zeroGradient';
                    self.Region.fluid['rho'].boundaryPatch = boundaryPatch;
        
                self.Region.fluid['rho'].cfdUpdateScale()
    
            self.Region.compressible='false' 

            
            if not 'mu' in transportKeys:
               
                boundaryPatch={} 
    
                self.Region.fluid['mu']=field.Field(self.Region,'mu','volScalarField')
                self.Region.fluid['mu'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                self.Region.fluid['mu'].phi.fill(1E-3)

                numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = 1;
                    boundaryPatch['type'] = 'zeroGradient';
                    self.Region.fluid['mu'].boundaryPatch = boundaryPatch;
        
                self.Region.fluid['mu'].cfdUpdateScale()

            
            if not 'Cp' in transportKeys:
               
                boundaryPatch={} 
    
                self.Region.fluid['Cp']=field.Field(self.Region,'Cp','volScalarField')
                self.Region.fluid['Cp'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                self.Region.fluid['Cp'].phi.fill(1004.)

                numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = 1;
                    boundaryPatch['type'] = 'zeroGradient';
                    self.Region.fluid['Cp'].boundaryPatch = boundaryPatch;
        
                self.Region.fluid['Cp'].cfdUpdateScale()


            if not 'k' in transportKeys:
                if 'DT' in transportKeys:
               
                    boundaryPatch={} 
                    
                    DTField = self.Region.fluid['DT'].phi
                    CpField = self.Region.fluid['Cp'].phi
                    rhoField = self.Region.fluid['rho'].phi            

                    self.Region.fluid['k']=field.Field(self.Region,'k','volScalarField')
                    self.Region.fluid['k'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                    self.Region.fluid['k'].phi= DTField*CpField*rhoField  
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                    
                    for iPatch in range(0,numberOfBPatches):
                        boundaryPatch['value'] = 1;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['k'].boundaryPatch = boundaryPatch;
            
                    self.Region.fluid['k'].cfdUpdateScale()


    def cfdReadThermophysicalProperties(self):
        
        thermophysicalPropertiesFilePath=self.Region.caseDirectoryPath+"/constant/thermophysicalProperties"
                        
        if not os.path.isfile(thermophysicalPropertiesFilePath):
            print('%s' %thermophysicalPropertiesFilePath)
            pass
    
        else:
            print('\n')
            print('Reading thermophysical properties ...')
    
            thermophysicalDicts=io.cfdReadAllDictionaries(thermophysicalPropertiesFilePath)
            thermophysicalKeys=list(thermophysicalDicts)   

            self.thermophysicalProperties={}
            self.thermophysicalProperties['thermoType'] = thermophysicalDicts['thermoType']
        
            
            if self.thermophysicalProperties['thermoType']['mixture']==['pureMixture']:
                specieBlock = self.thermophysicalProperties['thermoType']['specie']

                # Read and store the specie subdict
                specieList = thermophysicalDicts['mixture']['specie']
                
                for i in specieList: 
                    specieList[i]=float(specieList[i][0])
                
                self.thermophysicalProperties['mixture']={}
                self.thermophysicalProperties['mixture']['specie']={}
                self.thermophysicalProperties['mixture']['specie'].update(specieList)
                
                
                # Read and store the thermodynamics subdict    
                thermoList = thermophysicalDicts['mixture']['thermodynamics']    
                
                for i in thermoList: 
                    thermoList[i]=float(thermoList[i][0])
                    
                self.thermophysicalProperties['mixture']['thermodynamics']={}
                self.thermophysicalProperties['mixture']['thermodynamics'].update(thermoList)
                
                
                # Read and store the transport properties subdict    
                transportList = thermophysicalDicts['mixture']['transport']    
                
                for i in transportList: 
                    transportList[i]=float(transportList[i][0])
                    
                self.thermophysicalProperties['mixture']['transport']={}
                self.thermophysicalProperties['mixture']['transport'].update(transportList)
                
                
                # Read and store the transport model 
                if self.thermophysicalProperties['thermoType']['transport']==['const']:
        
                    print('\n Using transport model: const')
                    # Update mu 
                    muValue = self.thermophysicalProperties['mixture']['transport']['mu']
 
                    self.Region.fluid['mu']=field.Field(self.Region,'mu','volScalarField')
                    self.Region.fluid['mu'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                    self.Region.fluid['mu'].phi= [[muValue] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        boundaryPatch['value'] = muValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['mu'].boundaryPatch = boundaryPatch;
                        

                    # Update Pr
                    PrValue = self.thermophysicalProperties['mixture']['transport']['Pr']
 
                    self.Region.fluid['Pr']=field.Field(self.Region,'Pr','volScalarField')
                    self.Region.fluid['Pr'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                    self.Region.fluid['Pr'].phi= [[PrValue] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        boundaryPatch['value'] = PrValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['Pr'].boundaryPatch = boundaryPatch;

                elif self.thermophysicalProperties['thermoType']['transport']==['sutherland']:
                    print('\n Using transport model: sutherland')    

                    if not 'T' in self.Region.fluid.keys():
                        print('Sutherland model requires T, which is not there \n')
                        
                    else:
                        AsValue = self.thermophysicalProperties['mixture']['transport']['As'] # No pun intended
                        TsValue = self.thermophysicalProperties['mixture']['transport']['Ts']
                        TField = vars(self.Region.fluid['T'])
                        TField = np.array(TField['phi'])
                        # Update mu according to the sutherland law
     
                        self.Region.fluid['mu']=field.Field(self.Region,'mu','volScalarField')
                        self.Region.fluid['mu'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 

                        self.Region.fluid['mu'].phi= AsValue*np.sqrt(TField)/(1+np.divide(TsValue,TField))
        
                        numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
    
                        boundaryPatch={}                     
                        for iPatch in range(0,numberOfBPatches):
#                            boundaryPatch['value'] = muValue;
                            boundaryPatch['type'] = 'zeroGradient';
                            self.Region.fluid['mu'].boundaryPatch = boundaryPatch;
                        
                elif self.thermophysicalProperties['thermoType']['transport']==['polynomial']:
                    print('polynomial transport model not yet implemented, sorry\n')
                    sys.exit()

                else:
                    print('\nERROR: transport model in thermophysicalProperties not recognized. Valid entries are:')
                    print('const')
                    print('sutherland')
                    sys.exit()

####             Read and store the thermodynamics model 
                if self.thermophysicalProperties['thermoType']['thermo']==['hConst']:
                    print('\n Using thermodynamics model: hConst')                        
#               Update Cp 
                    CpValue = self.thermophysicalProperties['mixture']['thermodynamics']['Cp']
 
                    self.Region.fluid['Cp']=field.Field(self.Region,'Cp','volScalarField')
                    self.Region.fluid['Cp'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                    self.Region.fluid['Cp'].phi= [[CpValue] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        boundaryPatch['value'] = CpValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['Cp'].boundaryPatch = boundaryPatch;

#               Update k, thermal conductivity
                    PrValue = self.thermophysicalProperties['mixture']['transport']['Pr'] 

                    muField = vars(self.Region.fluid['mu'])
                    muField = np.array(muField['phi'])

                    CpField = vars(self.Region.fluid['Cp'])
                    CpField = np.array(CpField['phi'])
 
                    self.Region.fluid['k']=field.Field(self.Region,'k','volScalarField')
                    self.Region.fluid['k'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 

                    self.Region.fluid['k'].phi= np.multiply(muField,CpField)/PrValue
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        # boundaryPatch['value'] = kValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['k'].boundaryPatch = boundaryPatch;

                elif self.thermophysicalProperties['thermoType']['thermo']==['hPolynomial']:
                    print('hPolynomial transport model not yet implemented, sorry\n')
                    sys.exit()

                else:
                    print('\nERROR: thermodynamics model in thermophysicalProperties not recognized. Valid entries are:')
                    print('hConst')
                    sys.exit()


####             Read and store the Equation of State model 
                if self.thermophysicalProperties['thermoType']['equationOfState']==['perfectGas']:               
                    print('\n Using equationOfState model: perfectGas') 

                    self.Region.compressible=True

#               Update rho, density

                    TField = vars(self.Region.fluid['T'])
                    TField = np.array(TField['phi'])

                    PField = vars(self.Region.fluid['P'])
                    PField = np.array(PField['phi'])

                    molWeightValue = self.thermophysicalProperties['mixture']['specie']['molWeight'] 
                    RuValue = 8.314e3 # Universal gas constant in SI 
                    RbarValue = RuValue / molWeightValue # Gas constant in SI 

                    self.Region.fluid['rho']=field.Field(self.Region,'rho','volScalarField')
                    self.Region.fluid['rho'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 

                    self.Region.fluid['rho'].phi= np.divide(PField,RbarValue*TField)
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        # boundaryPatch['value'] = rhoValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['rho'].boundaryPatch = boundaryPatch;

                    self.Region.fluid['rho'].cfdUpdateScale()

#                   Update drhodp, (1/RT)
                    self.Region.fluid['drhodp']=field.Field(self.Region,'drhodp','volScalarField')
                    self.Region.fluid['drhodp'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 

                    self.Region.fluid['drhodp'].phi= np.divide(1,RbarValue*TField)
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        # boundaryPatch['value'] = drhodpValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['drhodp'].boundaryPatch = boundaryPatch;

                elif self.thermophysicalProperties['thermoType']['equationOfState']==['Boussinesq']: 
                    print('\n Using equationOfState model: Boussinesq') 

                    self.Region.compressible=True

#               Update rho, density

                    TField = vars(self.Region.fluid['T'])
                    TField = np.array(TField['phi'])

                    TRefValue = self.thermophysicalProperties['mixture']['thermodynamics']['TRef'] 
                    betaValue = self.thermophysicalProperties['mixture']['thermodynamics']['beta']                     
                    rhoRefValue = self.thermophysicalProperties['mixture']['thermodynamics']['rhoRef']                     


                    self.Region.fluid['rho']=field.Field(self.Region,'rho','volScalarField')
                    self.Region.fluid['rho'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 

                    auxTerm = 1-betaValue*(TField-TRefValue)

                    self.Region.fluid['rho'].phi= np.multiply(rhoRefValue,auxTerm)
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)

                    boundaryPatch={}                     
                    for iPatch in range(0,numberOfBPatches):
                        # boundaryPatch['value'] = rhoValue;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['rho'].boundaryPatch = boundaryPatch;

                    self.Region.fluid['rho'].cfdUpdateScale()

                elif self.thermophysicalProperties['thermoType']['equationOfState']==['incompressiblePerfectGas']: 
                    print('incompressiblePerfectGas equationOfState model not yet implemented, sorry\n')

                else:
                    print('\nERROR: equationOfState model in thermophysicalProperties not recognized. Valid entries are:')
                    print('Boussinesq')
                    print('perfectGas')

                            
                       