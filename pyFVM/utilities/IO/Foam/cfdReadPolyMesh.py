from pyFVM.src.mesh.IO.cfdReadPointsFile import cfdReadPointsFile
from pyFVM.src.mesh.IO.cfdReadFacesFile import cfdReadFacesFile
from pyFVM.src.mesh.IO.cfdReadOwnerFile import cfdReadOwnerFile
from pyFVM.src.mesh.IO.cfdReadNeighbourFile import cfdReadNeighbourFile
from pyFVM.src.mesh.IO.cfdReadBoundaryFile import cfdReadBoundaryFile
from pyFVM.src.mesh.cfdCheckIfCavity import cfdCheckIfCavity
from pyFVM.src.mesh.cfdProcessElementTopology import cfdProcessElementTopology
from pyFVM.src.mesh.cfdProcessNodeTopology import cfdProcessNodeTopology
from pyFVM.src.mesh.cfdProcessGeometry import cfdProcessGeometry


class cfdReadPolyMesh():
    
    def __init__(self,Region):
        print('Reading contents of ./constant/polyMesh folder ...')
        
        self.Region=Region
        self.Region.mesh = {}
        
        caseDirectoryPath = Region.caseDirectoryPath

        self.pointsFile = r"%s/constant/polyMesh/points" % caseDirectoryPath
        self.facesFile = r"%s/constant/polyMesh/faces" % caseDirectoryPath
        self.ownerFile = r"%s/constant/polyMesh/owner" % caseDirectoryPath
        self.neighbourFile = r"%s/constant/polyMesh/neighbour" % caseDirectoryPath
        self.boundaryFile = r"%s/constant/polyMesh/boundary" % caseDirectoryPath        
        
        
        self.Region.mesh['nodeCentroids'],self.Region.mesh['numberOfNodes']=cfdReadPointsFile(self.pointsFile)
        self.Region.mesh['faceNodes'],self.Region.mesh['numberOfFaces']=cfdReadFacesFile(self.facesFile)
        self.Region.mesh['owners']=cfdReadOwnerFile(self.ownerFile)
        self.Region.mesh['numberOfInteriorFaces'],self.Region.mesh['neighbours']=cfdReadNeighbourFile(self.neighbourFile)
        self.Region.mesh['numberOfBFaces']=self.Region.mesh['numberOfFaces']-self.Region.mesh['numberOfInteriorFaces']
        self.Region.mesh['numberOfElements'] = max(self.Region.mesh['neighbours'])+1 #because of zero indexing in Python
        self.Region.mesh['numberOfBElements']=self.Region.mesh['numberOfFaces']-self.Region.mesh['numberOfInteriorFaces']
        self.Region.mesh['cfdBoundaryPatchesArray'],self.Region.mesh['numberOfBoundaryPatches']=cfdReadBoundaryFile(self.boundaryFile)

        self.Region.mesh['closed']=cfdCheckIfCavity(self.Region.mesh)

        #these three are contained within cfdProcessTopolgy in uFVM
        cfdProcessElementTopology(self.Region.mesh)
        cfdProcessNodeTopology(self.Region.mesh)
        cfdProcessGeometry(self.Region.mesh)
        