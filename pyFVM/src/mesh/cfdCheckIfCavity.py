"""
Check if mesh is closed (cavity). Loop over the cfdBoundary patches and
check if no inlet or outlets exist. If true, then this case is said to be
a cavity case where a pressure is not fixed and has to be fixed later
"""

def cfdCheckIfCavity(mesh):
    foundPatch=False
    
    for patch, value in mesh['cfdBoundaryPatchesArray'].items():
        
        if value['type'] == 'inlet' or 'outlet':
            foundPatch =True
            
            break
        
    return foundPatch

