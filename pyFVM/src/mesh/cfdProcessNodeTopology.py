from pyFVM.src.mesh.cfdInvertConnectivity import cfdInvertConnectivity


def cfdProcessNodeTopology(mesh):
    
    mesh['nodeElements'] = cfdInvertConnectivity(mesh['elementNodes'])
    mesh['nodeFaces'] = cfdInvertConnectivity(mesh['faceNodes'])