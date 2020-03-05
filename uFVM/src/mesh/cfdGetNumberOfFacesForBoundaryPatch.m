function theNumberOfBFaces = cfdGetNumberOfFacesForBoundaryPatch(iBPatch)
%--------------------------------------------------------------------------
%
%  Written by the CFD Group @ AUB, Fall 2018
%  Contact us at: cfd@aub.edu.lb
%==========================================================================
% Routine Description:
%   
%--------------------------------------------------------------------------

global Region;

theNumberOfBFaces = Region.mesh.cfdBoundaryPatchesArray{iBPatch}.numberOfBFaces;
