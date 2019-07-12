
import os
import pyFVM.Region as Region

"""
Set Region as an instance of the Region class. The Region.Region.__init__
function is where everything is called into existence.
"""
region=Region.Region(os.getcwd())

#access Region's attributes
region_vars=vars(region)

#access mesh attributes
mesh=vars(region.mesh)














#cfdInitializeMdotFromU()
#
#U=region.fluid['U'].boundaryPatchRef
#
#phi = U
#
#theNumberOfComponents = len(phi[0])
#
#theNumberOfElements=Region.mesh.numberOfElements
#numberOfInteriorFaces = Region.mesh.numberOfInteriorFaces
#numberOfFaces = Region.mesh.numberOfFaces
#numberOfBFaces = Region.mesh.numberOfBFaces
#
#owners = cfdGetOwnersSubArrayForInteriorFaces()
#neighbours = cfdGetNeighboursSubArrayForInteriorFaces()
#g_f=cfdGetFaceWeightsSubArrayForInterior()
#
#theInterpolationScheme='linear'
#
#phi_f=[]
#phiInterior=phi[0:numberOfInteriorFaces]
#
#if theInterpolationScheme == 'linear':
#    for element, data in enumerate(phiInterior):
#        temp=[]
#        for component in range(theNumberOfComponents):
#            print(neighbours[element])
#            ai=g_f[element]*phiInterior[neighbours[element]][component]+(1-g_f[element])*phiInterior[owners[element]][component]
#            
#            temp.append(ai)
#            
#        phi_f.append(temp)
#        
#
#def cfdGetOwnersSubArrayForInteriorFaces():
#    
#    theNumberOfInteriorFaces = Region.mesh.numberOfInteriorFaces
#    owners = Region.mesh.owners[0:theNumberOfInteriorFaces]
#    
#    return owners
#
#def cfdGetNeighboursSubArrayForInteriorFaces():
#    
#    theNumberOfInteriorFaces = Region.mesh.numberOfInteriorFaces
#    neighbours = Region.mesh.neighbours[0:theNumberOfInteriorFaces]
#    
#    return neighbours
#
#def cfdGetFaceWeightsSubArrayForInterior():
#    
#    theNumberOfInteriorFaces = Region.mesh.numberOfInteriorFaces
#    faceWeights = Region.mesh.faceWeights[0:theNumberOfInteriorFaces]
#    
#    return faceWeights