import os
import pyFVM.IO as io
import pyFVM.Field as field
import pyFVM.Math as mth
import pyFVM.FoamDictionaries as fd
import numpy as np






#class FoamTimes():
    
#    def __init__(self, Region):
#        self.Region=Region
#        self.cfdInitTime(Region)
        
        
def cfdInitTime(self):
    self.time={}

    if self.dictionaries.controlDict['startFrom']=='startTime':
            self.time['currentTime'] = float(self.dictionaries.controlDict['startTime'])

    elif self.dictionaries.controlDict['startFrom']=='latestTime':
            self.time['currentTime'] = float(max(self.timeSteps))

    elif self.dictionaries.controlDict['startFrom']=='firstTime':
            self.time['currentTime'] = float(min(self.timeSteps))

    print('Start time: %.2f' % self.time['currentTime'])


def cfdUpdateRunTime(self):
    print('Fo so Yo')