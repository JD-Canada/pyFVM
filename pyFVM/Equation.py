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
                 
