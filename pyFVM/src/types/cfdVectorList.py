from numpy import zeros

#b=cfdVectorList([500,[2,3,4]])

def cfdVectorList(varargin):
    
    if not varargin:
        vectorList = []
    elif len(varargin)==1:
        
        n = varargin[0]
        
        vectorList = zeros((n, 3))
        
    elif len(varargin)==2:
        
        n     = varargin[0]
        
        value = varargin[1];
        
        vectorList = zeros((n, 3))
        
        for i in range(n):
        
            vectorList[i,:] = value
            
    
    return vectorList