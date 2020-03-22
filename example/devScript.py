
import os

import pyFVM.Region as Region
import numpy as np
import time as time
import numpy as np
import pyFVM.Field as field
import pyFVM.Math as math
import pyFVM.Interpolate as interpolate


start=time.time()
region=Region.Region(os.getcwd())
region_vars=vars(region)
print(time.time()-start)



    

