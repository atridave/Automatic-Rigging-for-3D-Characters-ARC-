import maya.cmds as cmds
import kinematics as km
import jointOperation as jo
import DailyTool as dt
import CurveOperation as co
reload(km)
reload(jo)
reload(dt)
reload(co)


class JointRigInfo(object):
    def __init__(self,startJoint):
        self.startJoint = startJoint
        self.joint =  jo.JointOperation()
        dtO = dt.DailyTool()
        self.stEd = self.joint.jointsInfo(self.startJoint,0)
        self.allJnts = self.joint.jointsInfo(self.startJoint,1)
        dtO.cls()
        
        
class SpineIkRig(JointRigInfo):
    def __init__(self,startJoint,numS,ctrlName,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
        JointRigInfo.__init__(self, startJoint)
        self.numS = numS
        self.ctrlChoice = ctrlChoice
        self.sx = sx
        self.sy = sy
        self.sz =sz
        self.color = color
        self.ctrlName = ctrlName
        self.ctrls = []
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.redi = redi
                      
        kmo = km.IKSpline(self.stEd[0], self.stEd[1])
        self.ikH = kmo.applyIk(self.numS)
        crv = co.CurveOperation(self.ikH[2]) 
        self.jntCtrls = crv.curveSkinCtrls(0,self.ctrlName)        
        
        for i in range(0,len(self.jntCtrls)):            
            kmg = km.ApplyConstrain(self.jntCtrls[i])
            kmg.makeOffGrp(2)
            co.MakeCtrl(self.jntCtrls[i]+'_ctrl',self.ctrlChoice,self.sx,self.sy,self.sz,self.color,1,self.jntCtrls[i],self.nx,self.ny,self.nz,self.redi)   
             
        comctrl = co.CtrlLib('dummy').addDummyShape()
        comShape = co.ShapeFinder(comctrl).shape
        comShape = cmds.rename(comShape,(self.ctrlName+'_commanAt'))
        cmds.select(comShape)
        cmds.addAttr( longName= 'stretchy', at = 'enum', en = ('off:on'), k =1)
            
        for i in range(0,len(self.jntCtrls)):
            cmds.parent(comShape,self.jntCtrls[i],add=1,s=1)
        cmds.delete(comctrl)
        
        con = km.MakeDisNode(self.ikH[2]).curveDisNode()
        cmds.connectAttr((comShape+'.stretchy'),(con+'.firstTerm'))
        conAttr = con+'.outColorR'        
        jo.jointScale(self.allJnts,'sx',conAttr)       
        
        twisterJnt = [self.jntCtrls[0],self.jntCtrls[-1]]
        twistJnt = [self.stEd[0],self.stEd[1]]
        
        for i in range(0,2):
            grp = cmds.group(em =1, n =(twistJnt[i]+'Twist_g'))
            delCon = km.ApplyConstrain(twistJnt[i],grp).pointOriCon(0)
            cmds.delete(delCon[0],delCon[1])
            cmds.parent(grp,twisterJnt[i])
        
        cmds.setAttr(self.ikH[0]+'.dTwistControlEnable',1)
        cmds.setAttr(self.ikH[0]+'.dWorldUpType',4)
        cmds.connectAttr((twistJnt[0]+'Twist_g.worldMatrix[0]'),(self.ikH[0]+'.dWorldUpMatrix'),f=1)
        cmds.connectAttr((twistJnt[1]+'Twist_g.worldMatrix[0]'),(self.ikH[0]+'.dWorldUpMatrixEnd'),f=1)
        




class FkCtrlRig(JointRigInfo):
    def __init__(self,startJoint,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
        JointRigInfo.__init__(self, startJoint)        
        self.ctrlChoice = ctrlChoice
        self.sx = sx
        self.sy = sy
        self.sz =sz
        self.color = color       
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.redi = redi
        for i in range(0,len(self.allJnts)):
            cmds.select(self.allJnts[i])
            co.MakeCtrl(self.allJnts[i]+'_ctrl',self.ctrlChoice,self.sx,self.sy,self.sz,self.color,1,self.allJnts[i],self.nx,self.ny,self.nz,self.redi)


class BipedSpineIKRig(SpineIkRig):
    def __init__(self,startJoint,numS,ctrlName,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
        SpineIkRig.__init__(self, startJoint, numS, ctrlName, ctrlChoice, sx, sy, sz, color, nx, ny, nz, redi)
        self.bipCtrls = ['cog','hip','waist','torso','chest']
        shapeChoise =  [5,4,1,5,1]
        shapeColor = [18,18,17,17,14]
        self.bipCtrlsG = []
        spineInctrlG = [dt.findParent(self.jntCtrls[0]).parent[0],dt.findParent(self.jntCtrls[2]).parent[0],dt.findParent(self.jntCtrls[1]).parent[0]]
        parentOrder = [0,0,2,3,1,3,0,1,0]
                      
        for i in range(0,len(self.bipCtrls)):
            co.MakeCtrl(self.bipCtrls[i]+'_ctrl',shapeChoise[i],3,3,3,shapeColor[i],1,self.bipCtrls[i],0,1,0,1)            
            self.bipCtrlsG.append(km.ApplyConstrain(self.bipCtrls[i]).makeOffGrp(2))
        
        
        self.bipCtrlsG.extend(spineInctrlG)        
        for i in range(0,len(self.bipCtrlsG)-1):
            cmds.parent(self.bipCtrlsG[i+1],self.bipCtrls[parentOrder[i]])
            
        hipRefPiv = km.ApplyConstrain(self.jntCtrls[1]).makeConGrp(2,'hipPiv')
        torsoRefPiv = km.ApplyConstrain(self.jntCtrls[1]).makeConGrp(2,'torsoPiv')
        km.ApplyConstrain(hipRefPiv,self.bipCtrlsG[-1]).parentCon(1)
        km.ApplyConstrain(torsoRefPiv,self.bipCtrlsG[-1]).parentCon(1)
        dt.parentIT(hipRefPiv,self.bipCtrls[1])
        dt.parentIT(torsoRefPiv,self.bipCtrls[3])
        
        for i in range(0,len(self.bipCtrlsG)):
            dt.LockHide(self.bipCtrlsG[i],1,1,1,1,1,1,1,1,1,1)
        
        dt.LockHide(self.bipCtrls[0],0,0,0,0,0,0,1,1,1,1,1)
        dt.LockHide(self.bipCtrls[1],0,0,0,0,0,0,1,1,1,1,1)
        dt.LockHide(self.bipCtrls[2],1,1,1,0,0,0,1,1,1,1,1)
        dt.LockHide(self.bipCtrls[3],0,0,0,0,0,0,1,1,1,1,1)
        dt.LockHide(self.bipCtrls[4],1,1,1,0,0,0,1,1,1,1,1)
            

class  BipedSpineIKFKRig(BipedSpineIKRig):
    def __init__(self,startJoint,numS,ctrlName,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
        BipedSpineIKFKRig.__init__(self, startJoint, numS, ctrlName, ctrlChoice, sx, sy, sz, color, nx, ny, nz, redi)
        self.bipCtrls = self.bipCtrls.append('midChestFK')
        self.bipCtrlsG.append(km.ApplyConstrain(self.bipCtrls[-1]).makeOffGrp(2))
        dt.parentIT(self.bipCtrlsG[5],self.bipCtrls[2])
        dt.parentIT(self.bipCtrlsG[3],self.bipCtrls[5])
        
    
        

        
    
    





        

        
        
        
# sel = cmds.ls(sl=1)
# for i in range(0,len(sel)):
#     FkCtrlRig(sel[0],2,1,1,1,6,1,0,0,5)

    
    

#aa =  SpineIkRig('joint1',25,'ropeCtrl',2,0.1,0.1,0.1,17)
        
    
    

#aa = BipedSpineIKRig('joint1',2,'spine',3,1,1,1,14,nx=None,ny=None,nz=None,redi=None)



 



  




        



   
        