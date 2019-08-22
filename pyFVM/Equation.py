import os

import pyFVM.Coefficients as coefficients
import pyFVM.Solve as solve
import pyFVM.Scalar as scalar
import pyFVM.Assemble as assemble

class Equation():
    
    def __init__(self, Region,fieldName):
        
        self.Region = Region
        
        self.name=fieldName
        
        self.initializeResiduals()
        
        
    def initializeResiduals(self):
        
        if self.name == 'U':
            self.rmsResidual =[1,1,1]
            self.maxResidual =[1,1,1]
            self.initResidual =[1,1,1]
            self.finalResidual =[1,1,1]
        else:
            self.rmsResidual = 1
            self.maxResidual = 1
            self.initResidual = 1
            self.finalResidual = 1                    
        
    def setTerms(self, terms):
        
        self.terms = terms
        
        
        
        
        
def cfdAssembleAndCorrectScalarEquation(self,theEquationName):

    self.coefficients=coefficients.Coefficients(self)
    
    # Pre-assemble
    cfdPreAssembleEquation(theEquationName)
    
    # Assemble Terms
    cfdAssembleEquationTerms(theEquationName)
    
    # Post Assemble Equation (under-relaxation, etc)
    cfdPostAssembleScalarEquation(theEquationName)    





def cfdPreAssembleEquation(theEquationName):
    pass


def cfdAssembleEquationTerms(self, theEquationName): # This function assembles equation terms"
    pass

    # get the scalar
    theEquation = cfdGetModel(self,theEquationName)        
    
    # Assemble coefficients 
    
    for iTerm in theEquation.terms:

        if iTerm == 'Transient':
            scalar.cfdZeroElementFLUXCoefficients(self)
            assemble.cfdAssembleTransientTerm(self,theEquationName)
        
        elif iTerm == 'Convection':
            print('It is convection')

        elif iTerm == 'Difussion':
            print('It is diffusion')

        elif iTerm == 'FalseTransient':
            print('It is false transient')
            
        else:
            print('\n%s\n' % (iTerm + ' term is not defined'))




def cfdPostAssembleScalarEquation(self, theEquationName):
    pass



def cfdGetModel(self,theFieldName):
    pass
    
    if theFieldName in self.model.keys():
        theModel = self.model[theFieldName]
    else:
        theModel = -1
 
    return theModel



