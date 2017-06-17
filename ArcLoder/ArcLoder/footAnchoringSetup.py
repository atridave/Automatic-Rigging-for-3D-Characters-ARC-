'''
Created on Jan 12, 2017

@author: adave
'''

import maya.cmds as cmds
import kinematics as km

driver = 'src:PlaneTargetLeft'
driven =  'src:PlaneWeightLeft'


def planeWeightSetupDoit(name,SourcePos):
    grp =  km.ApplyConstrain(SourcePos,name = name).makeConGrp(2)
    


planeWeightSetupDoit('LeftFootDisSt','R_Foot_Ctr')