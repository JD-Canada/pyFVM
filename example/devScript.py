
import os
import pyFVM_OOP.Region as Region

"""
Set Region as an instance of the Region class. The Region.Region.__init__
function is where everything is called into existence.
"""
Region=Region.Region(os.getcwd())

#access Region's attributes
region_vars=vars(Region)

#access mesh attributes
mesh=vars(Region.mesh)

#access attributes of a field
U=vars(Region.fluid['U'])
