'''
Created on May 26, 2017

@author: Admin
'''
import maya.cmds as cmds
import kinematics as km
import CurveOperation as co
import DailyTool as dt
reload(km)
reload(co)
reload(dt)

class rigMaker:
    
    def makePlacer(self,name,scale):
        cmds.select(cl=1)
        ctrls  = ['Placer','mover1','mover2']
        grps = km.rigHouseKeeping(name).makeAllHouseKeepingGroup(0)
        
       
        cmds.setAttr((grps[1]+'.visibility'),0)
        cmds.setAttr((grps[2]+'.overrideEnabled'),1)
        cmds.setAttr((grps[2]+'.overrideDisplayType'),2)           
         
        parent = grps[0]
        
        for i in range(0,len(ctrls)):
            ctrl = co.MakeCtrl(ctrls[i],1,scale,scale,scale,5,sp =None,spJnt = None,nx=0,ny=1,nz=0,redi=10,startConCtrl=None,endConCtrl=None)
            if i ==  0:
                attar =  km.AddDriverAttr(ctrl.ctrl,'RigScale',1,0.1,10,'float')               
                axies = ['.scaleX','.scaleY','.scaleZ']
                for j in range(0,3):
                    cmds.connectAttr((attar.name + '.' + attar.attrName),(ctrl.ctrl+axies[j]),f=1)       
                                                       
            dt.parentIT(ctrl.ctrl,parent)
            scale =  scale-0.3
            parent =  ctrl.ctrl 
            dt.LockHide(ctrl.ctrl,0,0,0,0,0,0,1,1,1,1)
            
    
    def makeArmRig(self,name,startJnt,poleVector,color,parent,globalCtrl):
        armRig = km.makeTwoJointIkFkRig(name,startJnt,poleVector,color,parent,globalCtrl)
    
    def makeBipadLegRig(self,name,startJnt,poleVector,color,parent,toeTipPivot,HeelPivot,globalCtrl):
        #quary from UI                        
        LegRig = km.makeTwoJointIkFkLegRig(name,startJnt,poleVector,color,parent,toeTipPivot,HeelPivot,globalCtrl)
    
    def makeClavicle(self,name,startJnt,color,parent):
        self.name  = name
        self.startJnt  =  startJnt
        clavicleRig = km.FkCtrlRig(self.startJnt,0,2,1,1.25,1,color,nx=None,ny=None,nz=None,redi=None)
        
        
    def makeHead(self,name,startJnt,color,parent):
        self.name  = name
        self.startJnt  =  startJnt
        headRig = km.FkCtrlRig(self.startJnt,0,7,1,1,1,color,nx=None,ny=None,nz=None,redi=None)
        
    def makeNeck(self,name,startJnt,color,parent):
        self.name  = name
        self.startJnt  =  startJnt
        neckRig =  km.SpineIkRig('neck01',2,(self.startJnt+'_ctrl'),1,1,1,1,17,0,1,0,1)
        
    def makeSplineIK(self,name,startJnt,color,parent,globalCtrl):
        self.name  = name
        self.startJnt  =  startJnt
        spine =  km.SpineIkRig('spine01',2,(self.startJnt+'_ctrl'),1,1,1,1,17,0,1,0,1,globalCtrl)
        
        
        


rigTNode  =  rigMaker().makePlacer('bipad',1)
#arm =  rigMaker().makeArmRig('L_2bIkFK_','L_Shoulder','L_ArmPole',13,'mover2','Placer')
#leg =  rigMaker().makeBipadLegRig('L_2bIkFK_','L_Thigh','L_LegPole',13,'mover2','toeTip','Heel','Placer')
#clavical =  rigMaker().makeClavicle('L_clavicle', 'L_clavicle', 13, 'mover2')
#head =  rigMaker().makeHead('Head', 'Head', 10, 'mover2')
#neck =  rigMaker().makeNeck('neck', 'neck01', 10, 'mover2')
spine =  rigMaker().makeSplineIK('spine', 'spine01', 10, 'mover2','Placer')


