'''
Created on 9 Nov 2015

@author: adave
'''




import kinematics as km
reload(km)
import maya.cmds as cmds

def hIKChrFix(jnts,move):
    print jnts
    loc = cmds.spaceLocator(p=(0,0,0), n= (jnts[0]+'temp_loc'))
    con = km.ApplyConstrain(jnts[0],loc[0]).pointCon(0)
    cmds.delete(con)
    cmds.move(move,0,0,r =1,ws =1)
    kmo = km.IKRP(jnts[0], jnts[2])
    ikH = kmo.applyIk()
    con = km.ApplyConstrain(loc[0],ikH[0]).pointCon(0)
    cmds.delete(con,loc[0])
    cmds.select(ikH[0])
    cmds.select(jnts[0])
    cmds.delete(ikH[0])
    


if __name__ == '__main__' :
    jnts = ['LeftArm','LeftForeArm','LeftHand']
    hIKChrFix(jnts,100)
    jnts = ['RightArm','RightForeArm','RightHand']
    hIKChrFix(jnts,-100)





