import time as timer



class Time():
    
    """Manages simulation's time related properties
    """
    
    def __init__(self,Region):
        
        ##Time at beginning of transient loop
        self.tic=timer.time()

        ##Instance of simulation's region class
        self.region=Region
        
        if self.region.dictionaries.controlDict['startFrom']=='startTime':
            
                ##Specified start time of the simulation
                self.startTime=float(self.region.dictionaries.controlDict['startTime'])
                
                ## The current time elapsed since the start of the simulation
                self.currentTime = self.startTime
    
        elif self.region.dictionaries.controlDict['startFrom']=='latestTime':
                self.currentTime = float(max(self.region.timeSteps))
    
        elif self.region.dictionaries.controlDict['startFrom']=='firstTime':
                self.currentTime = float(min(self.region.timeSteps))
    
        print('Start time: %.2f' % self.currentTime)
        
        ##Specified end time of the simulation
        self.endTime= float(self.region.dictionaries.controlDict['endTime'])
    
    def cfdUpdateRunTime(self):
        
        """Increments the simulation's runTime, updates cpu time
        """
        
        self.currentTime = self.currentTime + self.region.dictionaries.controlDict['deltaT']
        
        ## The elapsed cpu clock time since starting the transient loop
        self.cpuTime=timer.time()-self.tic
        
        print('cpu time: %0.4f [s]\n' % self.cpuTime)
        
    
    def cfdPrintCurrentTime(self):
        
        """Prints the current runTime"""
        
        print('\n\n Time: %0.4f [s]\n' % self.currentTime)
        
    def cfdDoTransientLoop(self):
        
        """
        Checks too see if simulation runTime has reached the simulation's end time
        """

        if self.currentTime < self.endTime:
            return True
        else:
            return False
        