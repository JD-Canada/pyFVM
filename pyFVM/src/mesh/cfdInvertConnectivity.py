

def cfdInvertConnectivity(theConnectivityArray):
    
    
    theInvertedSize=0
    
    for i in range(len(theConnectivityArray)):
        for j in range(len(theConnectivityArray[i])):
            
            theInvertedSize=max(theInvertedSize, int(theConnectivityArray[i][j]))
    
    theInvertedConnectivityArray = [[] for i in range(theInvertedSize+1)]
    
    for i in range(len(theConnectivityArray)):
        for j in range(len(theConnectivityArray[i])):
            theInvertedConnectivityArray[int(theConnectivityArray[i][j])].append(i)

    return theInvertedConnectivityArray