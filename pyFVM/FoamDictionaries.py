import os
import pyFVM.IO as io
import pyFVM.Field as field
import pyFVM.Math as mth


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
            print('\n\nReading Gravity ...\n')        
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
        
        print("\n")
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
            self.Region.timeDirectory='0' 
            
        else:
            print("Error in controlDict: startFrom is not valid!")
        
        for root, directory,files in os.walk(self.Region.caseDirectoryPath + "\\"+str(self.Region.timeDirectory)):

            if not files:
                print('Fields are not found in the %s directory' % (self.Region.caseDirectoryPath + "\\"+self.Region.timeDirectory+"!"))

        theNumberOfInteriorFaces = self.Region.mesh.numberOfInteriorFaces
        theNumberOfElements = self.Region.mesh.numberOfElements                       
                        
        for file in files:
            
            fieldName=file
            
            fieldFilePath=self.Region.caseDirectoryPath + "\\"+self.Region.timeDirectory+"\\"+fieldName
            
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
#                                print(list(value_str))
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
                            if self.Region.fluid[fieldName].type=='volScalarField' or Region.fluid[fieldName].type=='surfaceScalarField':
            
                                for count, subList in enumerate(Region.fluid[fieldName].phi):
                                    if count < iElementStart or count > iElementEnd:
                                        continue
                                    else:
                                        Region.fluid[fieldName].phi[count]=boundaryValue
                                        
                            if Region.fluid[fieldName].type=='volVectorField':
                                
                                for count, subList in enumerate(Region.fluid[fieldName].phi):
                                    if count < iElementStart or count > iElementEnd:
                                        continue
                                    else:
                                        Region.fluid[fieldName].phi[count]=boundaryValue
                        
                    except NameError:
                        continue
                    
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
            print('Reading transport properties ...')
    
            transportDicts=io.cfdReadAllDictionaries(transportPropertiesFilePath)
            transportKeys=list(transportDicts)   
    
            self.transportProperties={}
    
            for iKey in transportKeys:
                print(iKey)
                
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
                    self.Region.fluid[iKey].phi= [[keyValue] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]
            
            
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
                self.Region.fluid['rho'].phi= [[1.] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]

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
                self.Region.fluid['mu'].phi= [[1E-3] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]

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
                self.Region.fluid['Cp'].phi= [[1004.] for i in range(self.Region.mesh.numberOfElements+self.Region.mesh.numberOfBElements)]

                numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                
                for iPatch in range(0,numberOfBPatches):
                    boundaryPatch['value'] = 1;
                    boundaryPatch['type'] = 'zeroGradient';
                    self.Region.fluid['Cp'].boundaryPatch = boundaryPatch;
        
                self.Region.fluid['Cp'].cfdUpdateScale()


            if not 'k' in transportKeys:
                if 'DT' in transportKeys:
               
                    boundaryPatch={} 
                    kField=[]
                    
                    DTField = self.Region.fluid['DT'].phi
                    CpField = self.Region.fluid['Cp'].phi
                    rhoField = self.Region.fluid['rho'].phi            

                    for i in range(0,len(DTField)):
                        
                        kField.append([DTField[i][0]*CpField[i][0]*rhoField[i][0]])    
                    
        
                    self.Region.fluid['k']=field.Field(self.Region,'k','volScalarField')
                    self.Region.fluid['k'].dimensions=[0., 0., 0., 0., 0., 0.,0.] 
                    self.Region.fluid['k'].phi= kField
    
                    numberOfBPatches=int(self.Region.mesh.numberOfBoundaryPatches)
                    
                    for iPatch in range(0,numberOfBPatches):
                        boundaryPatch['value'] = 1;
                        boundaryPatch['type'] = 'zeroGradient';
                        self.Region.fluid['k'].boundaryPatch = boundaryPatch;
            
                    self.Region.fluid['k'].cfdUpdateScale()


                            
                       