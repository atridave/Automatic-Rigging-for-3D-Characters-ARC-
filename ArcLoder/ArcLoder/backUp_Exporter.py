'''
Created on 27 May 2016

@author: adave
'''
import maya.cmds as cmds

def _daveHeadCamHack(self):
    print 'It is '
    _fileName  =  cmds.file( q=True, sn=1)
    for i in range(0,20):
        print _fileName
        
    targetJnt = 'rig:src:Head_LowPass'
    head = 'rig:Head_Ctr'
    locoCtr = 'rig:Locomotion_Ctr'
    posCon = cmds.pointConstraint(head,targetJnt)
    cmds.delete(posCon)
    parentCon = cmds.parentConstraint(locoCtr,targetJnt,mo=1)
    startFrame = cmds.playbackOptions(q=1,min =1)
    endFrame = cmds.playbackOptions(q=1,max =1)
    cmds.bakeResults(targetJnt, t=(startFrame,endFrame),at=['tx','ty','tz',"rx","ry","rz"], simulation=True )
    cmds.delete(parentCon)
    cmds.file(save=1,type = 'mayaAscii',f=1)
    print ('I am saving ::::::::::::::::'+  _fileName)