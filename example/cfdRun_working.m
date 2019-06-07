%--------------------------------------------------------------------------
%
%  written by the CFD Group @ AUB, 2018
%  contact us at: cfd@aub.edu.lb
%==========================================================================
% Case Description:
%     In this test case the square cavity problem is considered with a
%     uniform velocity profile throughout the domain. The objective is to
%     investigate the convection schemes (the default now is set to first
%     order upwind). The equation to be solved is given by the following
%     pde: d(rho*phi)/dt + div(rho*U*phi) = 0
%--------------------------------------------------------------------------

% Initialize
cfdStartSession;

% Read OpenFOAM Files
cfdReadOpenFoamFiles;

global Region;

controlDict = Region.foamDictionary.controlDict;
    
if strcmp(controlDict.startFrom, 'startTime')
     timeDirectory = num2str(controlDict.startTime);
elseif strcmp(controlDict.startFrom, 'firstTime')
     timeDirectory = '0';
elseif strcmp(controlDict.startFrom, 'latestTime')
     timeDirectories = cfdGetTimeSteps;
     timeDirectory = num2str(max(timeDirectories));
else
     error('\nError in controlDict. startFrom is not valid\n');
  end

% Case directory
caseDirectoryPath = cfdGetCaseDirectoryPath;

% Read field
files = dir([caseDirectoryPath, filesep, timeDirectory]);

if isempty(files)
    error('\n%s\n', ['Fields are not found in the ', timeDirectory,' directory']);
end

% Get mesh
theMesh = cfdGetMesh;
theNumberOfElements = cfdGetNumberOfElements;
theNumberOfInteriorFaces = cfdGetNumberOfInteriorFaces;

for iFile=1:length(files)
    if (files(iFile).bytes)==0 || (files(iFile).isdir)
        continue;
    end
    
    % get field name from file name
    fieldName = files(iFile).name;
    fieldFilePath = [caseDirectoryPath, filesep, timeDirectory, filesep, fieldName];
    
    % Open field in read mode
    fid = fopen(fieldFilePath, 'r');
    
    % Initialize header
    header = cell(0);
    
    % Scan/Read header
    while ~feof(fid)
        tline = fgetl(fid);
        
        % Skip empty lines
        tline = cfdSkipEmptyLines(fid, tline);
        
        % Skip macro-commented section
        tline = cfdSkipMacroComments(fid, tline);
        
        % Skip commented lines
        tline = cfdSkipCommentedLine(fid, tline);
        
        % read header block
        if cfdContains(tline, 'FoamFile')
            if isempty(header)
                header = cfdReadCfdDictionary(fid, 'FoamFile');
            else
                break;
            end
        else
            if ~isempty(header)
                break;
            end
        end
    end
    
    % Setup mesh field
    cfdSetupMeshField(fieldName, header.class);
    
    % Store initial value in mesh field
    theMeshField = cfdGetMeshField(fieldName);
    
    % Read dimensions
    theMeshField.dimensions = cfdGetKeyValue('dimensions', 'dimensions', fid);
    
    % Read and store internal field
    internalField = cfdGetKeyValue('internalField', 'string', fid);
    C = textscan(internalField, '%s', 1);
    valueType = C{1}{1};
    
    if strcmp(theMeshField.type, 'surfaceScalarField')
        
        if strcmp(valueType, 'uniform')
            value_str = textscan(internalField, 'uniform %f;', 1);
            theMeshField.phi(1:theNumberOfInteriorFaces) = value_str{1};
        elseif strcmp(valueType, 'nonuniform')
            theMeshField.phi(1:theNumberOfInteriorFaces) = cfdReadNonuniformList('internalField', fieldFilePath);
        end
        
        % Read and store cfdBoundary field
        boundaries = theMesh.cfdBoundaryPatchesArray;
        theNumberOfBPatches = length(boundaries);
        
        for iBPatch=1:theNumberOfBPatches
            
            % Get info
            theBCInfo = boundaries{iBPatch};
            iFaceStart = theBCInfo.startFaceIndex;
            iFaceEnd = iFaceStart+theBCInfo.numberOfBFaces-1;
            
            
            % Get field cfdBoundary condition
            type = cfdGetKeyValueFromBlock('type', ['boundaryField/', theBCInfo.name], fieldFilePath);
            
            % Store field cfdBoundary condition
            boundaryPatchRef.type = type;
            
            % Read cfdBoundary value
            value = cfdGetKeyValueFromBlock('value', ['boundaryField/', theBCInfo.name], fieldFilePath);
            
            if isempty(value)
                boundaryPatchRef.value = 0;
                
                theMeshField.boundaryPatchRef{iBPatch} = boundaryPatchRef;
                
                % Clear boundaryPatchRef
                structureFields = fieldnames(boundaryPatchRef);
                for structureFieldName=structureFields
                    boundaryPatchRef = rmfield(boundaryPatchRef, structureFieldName);
                end
                
                continue;
            end
            
            C = textscan(value, '%s', 1);
            valueType = C{1}{1};
            
            boundaryPatchRef.valueType = valueType;
            
            if strcmp(valueType, 'uniform')
                value_str = textscan(value, 'uniform %f', 1);
                theMeshField.phi(iFaceStart:iFaceEnd) = value_str{1};
                boundaryPatchRef.value = value_str{1};
            elseif strcmp(valueType, 'nonuniform')
                valueList = cfdReadNonuniformList(theBCInfo.name, fieldFilePath);
                theMeshField.phi(iFaceStart:iFaceEnd) = valueList;
                boundaryPatchRef.value = valueList;
            end
            
            theMeshField.boundaryPatchRef{iBPatch} = boundaryPatchRef;
            
        end
        
    else
        
        if strcmp(valueType, 'uniform')
            if strcmp(theMeshField.type, 'volScalarField')
                value_str = textscan(internalField, 'uniform %f;', 1);
                theMeshField.phi(1:theNumberOfElements) = value_str{1};
            elseif strcmp(theMeshField.type, 'volVectorField')
                value_str = textscan(internalField, 'uniform (%f %f %f);', 1);
                for iElement=1:theNumberOfElements
                    theMeshField.phi(iElement,:) = [value_str{1}, value_str{2}, value_str{3}];
                end
            end
        elseif strcmp(valueType, 'nonuniform')
            theMeshField.phi(1:theNumberOfElements, :) = cfdReadNonuniformList('internalField', fieldFilePath);
        end
        
        % Read and store cfdBoundary field
        boundaries = theMesh.cfdBoundaryPatchesArray;
        theNumberOfBPatches = length(boundaries);
        
        for iBPatch=1:theNumberOfBPatches
            
            % Get info
            theBCInfo = boundaries{iBPatch};
            
            numberOfBFaces = theBCInfo.numberOfBFaces;
            iFaceStart = theBCInfo.startFaceIndex;
            
            iElementStart = theNumberOfElements+iFaceStart-theNumberOfInteriorFaces;
            iElementEnd = iElementStart+numberOfBFaces-1;
            
            
            % Get field cfdBoundary condition
            type = cfdGetKeyValueFromBlock('type', ['boundaryField/', theBCInfo.name], fieldFilePath);
            
            % Store field cfdBoundary condition
            boundaryPatchRef.type = type;
            
            % Read cfdBoundary value
            value = cfdGetKeyValueFromBlock('value', ['boundaryField/', theBCInfo.name], fieldFilePath);
        end  
    end
    
% key='value'
% blockName=['boundaryField/', theBCInfo.name]
% 
% fileID = fopen(fieldFilePath, 'r');
% 
% % if nargin==3
% %     cfdSkipHeader = true;
% % else
% %     cfdSkipHeader = varargin{1};
% % end
% 
% %Skip Header
% cfdSkipHeader=true;
% if cfdSkipHeader
%     for i=1:16
%         fgetl(fileID);
%     end
% end
% 
% value = '';
% 
% % Check if required block is a subblock
% nSubBlocks = length(strfind(blockName, '/'));
% if nSubBlocks>0
%     blockNames = textscan(blockName, '%s', nSubBlocks+1, 'delimiter', '/');
%     blockNames = blockNames{1};
% else
%     blockNames = {blockName};
% end
% 
% iBlock = 1;
% while(~feof(fileID))
%     % Read each line
%     tline = fgetl(fileID);
%     
%     % Skip empty lines
%     if isempty(tline)
%         continue;
%     end
%     
%     % Skip empty lines
%     if isempty(strrep(tline, ' ', ''))
%         continue;
%     end
%     
%     % Skip commented lines
%     if length(tline)>1
%         if strcmp(tline(1:2), '//')
%             continue;
%         end
%     end
%     
%     % Search for the block name
%     C = textscan(tline, '%s', 1);
%     if strcmp(C{1}{1}, blockNames{iBlock})
%         if length(blockNames)~=iBlock
%             iBlock = iBlock + 1;
%             continue;
%         end
%     else
%         continue;
%     end
%     
%     % Skip to content
%     tline = fgetl(fileID);
%     tline = fgetl(fileID);
%     
%     % Collect value
%     C = textscan(tline, '%s %[^\n]', 1);
%     entry = C{1}{1};
%     while ~strcmp(key, entry)
%         tline = fgetl(fileID);
%         
%         if tline<0
%             value = '';
%             return;
%         end
%         
%         % Skip empty lines
%         if isempty(tline)
%             continue;
%         end
%         
%         % Skip empty lines
%         if isempty(strrep(tline, ' ', ''))
%             continue;
%         end        
%         
%         % Skip commented lines
%         if length(tline)>1
%             if strcmp(tline(1:2), '//')
%                 continue;
%             end
%         end
%         
%         C = textscan(tline, '%s %[^\n]', 1);
%         entry = C{1}{1};
%     end
%     semicolonLocation = strfind(C{2}{1}, ';');
%     if ~isempty(semicolonLocation)
%         value = C{2}{1}(1:semicolonLocation-1);
%     else
%         value = C{2}{1};
%     end
%     fclose(fileID);
%     return;
% end
%             if isempty(value)
%                 if strcmp(theMeshField.type, 'volScalarField') || strcmp(theMeshField.type, 'surfaceScalarField')
%                     boundaryPatchRef.value = 0;
%                 elseif strcmp(theMeshField.type, 'volVectorField')
%                     boundaryPatchRef.value = [0,0,0];
%                 end
%                 
%                 theMeshField.boundaryPatchRef{iBPatch} = boundaryPatchRef;
%                 
%                 % Clear boundaryPatchRef
%                 structureFields = fieldnames(boundaryPatchRef);
%                 for structureFieldName=structureFields
%                     boundaryPatchRef = rmfield(boundaryPatchRef, structureFieldName);
%                 end
%                 
%                 continue;
%             end
%             
%             C = textscan(value, '%s', 1);
%             valueType = C{1}{1};
%             
%             boundaryPatchRef.valueType = valueType;
%             
%             if strcmp(valueType, 'uniform')
%                 if strcmp(theMeshField.type, 'volScalarField') || strcmp(theMeshField.type, 'surfaceScalarField')
%                     value_str = textscan(value, 'uniform %f', 1);
%                     theMeshField.phi(iElementStart:iElementEnd) = value_str{1};
%                     boundaryPatchRef.value = value_str{1};
%                 elseif strcmp(theMeshField.type, 'volVectorField')
%                     value_str = textscan(value, 'uniform (%f %f %f)', 1);
%                     for iBElement=iElementStart:iElementEnd
%                         theMeshField.phi(iBElement,:) = [value_str{1}, value_str{2}, value_str{3}];
%                     end
%                     boundaryPatchRef.value = [value_str{1}, value_str{2}, value_str{3}];
%                 end
%             elseif strcmp(valueType, 'nonuniform')
%                 valueList = cfdReadNonuniformList(theBCInfo.name, fieldFilePath);
%                 theMeshField.phi(iElementStart:iElementEnd, :) = valueList;
%                 boundaryPatchRef.value = valueList;
%             end
%             
%             theMeshField.boundaryPatchRef{iBPatch} = boundaryPatchRef;
%             
%         end
%         
%         % Clear boundaryPatchRef
%         structureFields = fieldnames(boundaryPatchRef);
%         for structureFieldName=structureFields
%             boundaryPatchRef = rmfield(boundaryPatchRef, structureFieldName);
%         end
%     end
%     
%     % Store mesh field in data base
%     cfdSetMeshField(theMeshField);
%     
%     % Update field for boundary patches
%     if strcmp(theMeshField.type, 'volScalarField')
%         cfdUpdateScalarFieldForAllBoundaryPatches(theMeshField.name);
%     else
%         cfdUpdateVectorFieldForAllBoundaryPatches(theMeshField.name);
%     end
end
