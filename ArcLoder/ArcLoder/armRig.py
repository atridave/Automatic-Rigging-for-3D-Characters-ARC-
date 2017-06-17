'''
Created on Sep 1, 2016

@author: adave
'''
import maya.cmds as cmds
import jointOperation as jo
import kinematics as km
import CurveOperation as co
import spineRig as sp
import DailyTool as dt
reload(co)
reload(jo)
reload(km)
reload(dt)
  
class makeTwoJointIkFkRig:
    def __init__(self,rigName,startJoint,poleCtrl,ctrlColor,rigParent, gCtrl=None):
        self.startJont  =  startJoint
        self.poleCtrl =  poleCtrl        
        self.ikFkCon = []
        self.ctrlColor = ctrlColor
        self.gCtrl =  gCtrl
        self.rigName =  rigName
        self.rigParent  = rigParent

        
        self.sourceJnt  =  jo.JointOperation().jointsInfo(self.startJont,1)
        self.topG =  km.ApplyConstrain(self.startJont).makeOffGrp(2,(self.startJont+'Rig'))
        
        # making IkHendle Ctrl
        self.ikHJnt =  jo.JointOperation().makeDuplicateJointChaines(self.sourceJnt[2],self.sourceJnt[2],'_Ikctrl')
        
        #adding attributes 
        cmds.select(self.ikHJnt[0])
        km.AddDriverAttr(self.ikHJnt[0],'upperLimb',0,-10,10,'float')
        km.AddDriverAttr(self.ikHJnt[0],'lowerLimb',0,-10,10,'float')
        cmds.addAttr(ln= 'ikFK',at = 'enum',en = 'Ik:fk',k=1)
        km.AddDriverAttr(self.ikHJnt[0],'stretchy',None,None,None,'bool')
            
        co.MakeCtrl(self.ikHJnt[0]+'_ctrl',2,0.5,0.5,0.5,ctrlColor,1,self.ikHJnt[0])
        self.ikHJntG = km.ApplyConstrain(self.ikHJnt[0]).makeOffGrp(2)
        
               
        #make ikFk Chain and connect it to ikHandle
        self.ikJnt =  jo.JointOperation().makeDuplicateJointChaines(self.startJont,self.startJont, '_ik')
        self.ikJntG = km.ApplyConstrain(self.ikJnt[0]).makeOffGrp(2)
        self.fkJnt = jo.JointOperation().makeDuplicateJointChaines(self.startJont,self.startJont, '_fk')
        self.fkJntG = km.ApplyConstrain(self.fkJnt[0]).makeOffGrp(2)
        cmds.parent(self.ikJntG,self.topG)
        cmds.parent(self.fkJntG,self.topG)
        
        self.rev =  cmds.createNode('reverse',n = (self.startJont+'ikFk_rev'))
        cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.rev+'.inputX'))
                 
        for i in range(0,len(self.sourceJnt)):
            self.ikCon = km.ApplyConstrain(self.ikJnt[i],self.sourceJnt[i]).parentCon(0)
            self.fkCon = km.ApplyConstrain(self.fkJnt[i],self.sourceJnt[i]).parentCon(0)
            conW =  cmds.parentConstraint(self.ikCon,q=1 ,wal=1)
            cmds.connectAttr((self.rev+'.outputX'),(self.ikCon[0]+'.'+conW[0]))
            cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.ikCon[0]+'.'+conW[1]))
               
        #make FK rig
        
        sp.FkCtrlRig(self.fkJnt[0],1,1,1,1,self.ctrlColor,1,0,0,2)
        cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.fkJntG+'.visibility'))
                   
        
        km.ApplyConstrain(self.ikHJnt[0], self.ikJnt[2]).orientCon(0)        
        co.MakeCtrl(self.poleCtrl+'_ctrl',2,0.5,0.5,0.5,ctrlColor,1,self.poleCtrl)
        self.refLine = co.MakeCtrl(self.ikJnt[1]+'Ref_ctrl',6,1,1,1,13,startConCtrl=self.ikJnt[1],endConCtrl=self.poleCtrl)
       
          
          
            
        ikH =  km.twoJointIk(self.ikJnt[0],self.poleCtrl)
        cmds.parent(ikH.ikH[0],self.ikHJnt[0])
        self.poleCtrlG = km.ApplyConstrain(self.poleCtrl).makeOffGrp(2)
        km.ApplyConstrain(self.ikJntG,self.poleCtrlG ).pointCon(1)
        km.ApplyConstrain(self.ikHJnt,self.poleCtrlG ).pointCon(1)
        cmds.connectAttr((self.rev+'.outputX'),(self.ikJntG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.ikHJntG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.poleCtrlG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.refLine.name+'.visibility'))
        

        #make fkJoint stretchy makeStetchyFK(self,attrName,scaleAxies)
        km.makeStretchy(self.fkJnt[0]).makeStetchyFK('stretch','scaleX')
        km.makeStretchy(self.ikJnt[0],self.gCtrl).makeStretchyIK(self.ikHJnt[0])
       
        
        #Housekeeping Groups
        rigCG = [self.topG,self.ikHJntG,self.poleCtrlG]
        rigPG = [self.rigParent,self.rigParent,self.rigParent]
        rigG = [rigCG,rigPG]
        kinematicsG = [(self.ikJntG+'_disNode_g'),self.refLine.hkG]
        helperG = [self.refLine.ctrl]
        km.rigHouseKeeping(self.rigName).rigParent(rigG, kinematicsG, helperG)
        cmds.setAttr((ikH.ikH[0]+'.visibility'),0)

 
#aa = makeTwoJointIkFkRig('L_2bIkFK_','L_Shoulder','L_ArmPole',13,'mover2',gCtrl=None)


