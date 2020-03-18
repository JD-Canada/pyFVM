
import os

import pyFVM.Region as Region
import numpy as np
import time as time

start=time.time()
region=Region.Region(os.getcwd())
region_vars=vars(region)
print(time.time()-start)
