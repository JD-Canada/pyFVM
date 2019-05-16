import numpy as np
from pyFVM.utilities.IO.File.cfdSkipEmptyLines import cfdSkipEmptyLines
from pyFVM.utilities.IO.File.cfdSkipMacroComments import cfdSkipMacroComments
from pyFVM.utilities.IO.File.cfdReadCfdDictionary import cfdReadCfdDictionary
from pyFVM.src.types.cfdVector import cfdVector
from pyFVM.src.types.cfdVectorList import cfdVectorList


def cfdReadPointsFile(pointsFile):
    
    
    with open(pointsFile,"r") as fpid:
        
        print('Reading points file ...')
        points_x=[]
        points_y=[]
        points_z=[]
        
        for linecount, tline in enumerate(fpid):
            
            if not cfdSkipEmptyLines(tline):
                continue
            
            if not cfdSkipMacroComments(tline):
                continue
            
            if "FoamFile" in tline:
                dictionary=cfdReadCfdDictionary(fpid)
                continue

            if len(tline.split()) ==1:
                if "(" in tline:
                    continue
                if ")" in tline:
                    continue
                else:
                    numberOfPoints = int(tline.split()[0])
                    continue
            
            tline=tline.replace("(","")
            tline=tline.replace(")","")
            tline=tline.split()
            
            points_x.append(float(tline[0]))
            points_y.append(float(tline[1]))
            points_z.append(float(tline[2]))
    
    nodeCentroids = np.array((points_x, points_y, points_z), dtype=float).transpose()
#    nodeCentroids=pd.DataFrame({'x': points_x, 'y': points_y, 'z': points_z})
    numberOfNodes=numberOfPoints
    
    return nodeCentroids, numberOfNodes

    