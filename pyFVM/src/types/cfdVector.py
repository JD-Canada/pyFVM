from numpy import zeros

def cfdVector(varargin):
    
    if not varargin:
       
        theVector = zeros((1,3))
        
    elif len(varargin) == 1:
        
        theVector = varargin[0]
        
    elif len(varargin) == 3:
        
        theVector = [varargin[0], varargin[1], varargin[2]]
        
    else:
        
        print('Bad definition of cfdVector')
        
    return theVector