'''
Created on Sep 8, 2016

@author: adave
'''
import inspect,os


import CORE.rigTemplate.rt as rtL
rtL.checkIt()



aa = inspect.currentframe()
print 'I  am getting loaded from '
print __file__
print inspect.getfile(aa)


inspect