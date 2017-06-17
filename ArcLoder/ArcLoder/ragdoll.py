'''
Created on Dec 7, 2016

@author: adave
'''
import kinematics as km
import maya.cmds as cmds

def makeRagDollSetup():
    sel =  cmds.ls(sl=1)
    suffix =  '_Phys'
    parentSuffix =  '_PhysParentFrame'
    for i in range(0,len(sel)):
        cmds.select(cl=1)
        locPhy = cmds.spaceLocator(n= (sel[i]+suffix))
        locPhy =  cmds.ls(sl=1,l=1)
        pLocPhys = cmds.spaceLocator(n= (sel[i]+parentSuffix))
        pLocPhys = cmds.ls(sl=1,l=1)
        cmds.select(pLocPhys)
        cmds.parent(locPhy,pLocPhys)
        con = km.ApplyConstrain(sel[i],pLocPhys).pointOriCon(0)
        cmds.delete(con[0],con[1])
        _parentIt(sel[i],pLocPhys)
        
    
def _parentIt(jnt,pFrameLoc):
    suffix =  'ParentFrame'
    parent = cmds.listRelatives((jnt),p=1)
#     print parent
#     ##check if has _phy and _phyFrame
#     print (parent[0]+'_Phys')
#     print (parent[0]+'_PhysParentFrame')
#     #objEx = cmds.objExists(parent[0]+'_Phys')
    if cmds.objExists(parent[0]+'_Phys') and cmds.objExists(parent[0]+'_PhysParentFrame'):
        cmds.parent(pFrameLoc,(parent[0]+'_Phys'))
        
    else:
        print 'cant parent'
        
    


makeRagDollSetup()