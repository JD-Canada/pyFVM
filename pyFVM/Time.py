import os
import pyFVM.IO as io
import pyFVM.Field as field
import pyFVM.Math as mth
import pyFVM.FoamDictionaries as fd
import numpy as np



def cfdInitTime(self):
    
    ## current time of simulation. Its value changes depending on how the simulation is initialized. 
    self.time={}

    if self.dictionaries.controlDict['startFrom']=='startTime':
            self.time['currentTime'] = float(self.dictionaries.controlDict['startTime'])

    elif self.dictionaries.controlDict['startFrom']=='latestTime':
            self.time['currentTime'] = float(max(self.timeSteps))

    elif self.dictionaries.controlDict['startFrom']=='firstTime':
            self.time['currentTime'] = float(min(self.timeSteps))

    print('Start time: %.2f' % self.time['currentTime'])

def cfdUpdateRunTime(self):
    self.time['currentTime'] = self.time['currentTime'] + self.dictionaries.controlDict['deltaT']
    # There should be a physical time registry here, I can't see where it does start in Matlab

def cfdPrintCurrentTime(self):
    print('\n\n Time: %0.4f [s]\n' % self.time['currentTime'])