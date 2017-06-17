import maya.cmds as cmds
import DailyTool as dt
import CurveOperation as co
import jointOperation as jo
reload(jo)



class IKHandle:
    
    def __init__(self,startJoint,endJoint):
        self.startJoint = startJoint
        self.endJoint = endJoint
        
    def applyIk(self,startJoint,endJoint):
        pass


class IKRP(IKHandle):
            
    def applyIk(self):
        self.ik = cmds.ikHandle(sj = self.startJoint,ee= self.endJoint,n=(self.startJoint+'_ikH'),sol = 'ikRPsolver')
        ikr = IKRenamer(self.startJoint,self.endJoint)
        self.ikH = ikr.renameikH(self.ik)   
        return self.ikH
   

class IKSpring(IKHandle):
            
    def applyIk(self,startJoint,endJoint):
        self.ikH = cmds.ikHandle(sj = self.startJoint,ee= self.endJoint,n=(self.startJoint+'_ikH'),sol = 'ikRPsolver')


class IKSpline(IKHandle):
                
    def applyIk(self,numS):
        self.ik = cmds.ikHandle(sj = self.startJoint,ee= self.endJoint,n=(self.startJoint+'_ikH'),sol = 'ikSplineSolver',ccv =1,ns=numS)
        ikr = IKRenamer(self.startJoint,self.endJoint)
        self.ikH = ikr.renameikH(self.ik)
        return self.ikH


class IKRenamer(IKHandle):
        
    def renameikH(self,ik):
        self.ik = ik
        cmds.rename(self.ik[1],(self.startJoint+'_eff'))
        self.ik[1] = self.ik[1].replace(self.ik[1],(self.startJoint+'_eff'))
        num = len(self.ik)
        if num == 3:
            cmds.rename(self.ik[2],(self.startJoint+'_crv'))
            self.ik[2] = self.ik[2].replace(self.ik[2],(self.startJoint+'_crv'))
        return self.ik


    
    
class twoJointIk:
    def __init__(self,startJoint,endJoint,poleVec= None):
        self.startJoint =  startJoint
        self.poleVec = poleVec
        self.endJoint =  endJoint
        self.stEd = jo.JointOperation().jointsInfo(self.startJoint,1)
        self.ikH = IKRP(self.startJoint,self.stEd[self.endJoint]).applyIk()
        if self.poleVec:
            self.poleCon = ApplyConstrain(self.poleVec,self.ikH[0]).poleVecCon()
        cmds.setAttr((self.ikH[0]+'.visibility'),0)


class makeStretchy:
    def __init__(self,startJoint,gCtrl=None):
        self.startJoint = startJoint
        self.gCtrl =  gCtrl
    
    def makeStetchyFK(self,attrName,scaleAxies):
        self.jnts =  jo.JointOperation().jointsInfo(self.startJoint,1)
        for i in range(0,len(self.jnts)-1):
            AddDriverAttr(self.jnts[i],attrName,0,0,10,'float')
            self.makeStretchyCore(self.jnts[i], attrName, self.jnts[i], scaleAxies)            
            
    def makeLimbStretch(self,driverattr,driven, drivenattr,pmaName=None):
        return self.makeStretchyCore(self.startJoint, driverattr, driven, drivenattr,pmaName)
    
    
    def makeStretchyIK(self,ikdriver,TwoBIK = None):        
        #combine libstretch and here with limb scale
        parent = dt.findParent(self.startJoint).parent[0]
        ikJnt =  jo.JointOperation().jointsInfo(self.startJoint, 1)
        length = jo.JointOperation().jointLengthInfo(self.startJoint,TwoBIK)
        
        upperLimbPma = makeStretchy(ikdriver).makeLimbStretch('upperLimb', ikJnt[0], 'scaleX',ikJnt[0])
        lowerLimbPma = makeStretchy(ikdriver).makeLimbStretch('lowerLimb', ikJnt[1], 'scaleX',ikJnt[1])
              
        dis = MakeDisNode(parent,ikdriver,length,self.gCtrl).LocDisNode()
               
        cmds.connectAttr((dis+'.outColorR'), (upperLimbPma+'.input1D[1]'),f=1)
        cmds.connectAttr((dis+'.outColorR'), (lowerLimbPma+'.input1D[1]'),f=1)
        
        return dis 
    

    
    def makeStretchyCore(self,driver,driverattr,driven,drivenattr,pmaName=None):
        if pmaName == None:
            pmaName = driver                      
        pma = cmds.createNode('plusMinusAverage',n = (pmaName+'stretch_pma'))
        cmds.connectAttr((driver+'.'+driverattr), (pma+'.input1D[0]'),f=1)
        cmds.setAttr(pma+'.input1D[1]',1)
        cmds.connectAttr((pma+'.output1D'),(driven+'.'+drivenattr),f=1)
                        
        return pma       
        
    
class ApplyConstrain:
    
    def __init__(self,source,target=None):
        self.source = source
        self.target = target        
        
    def pointCon(self,moV):
        self.con = cmds.pointConstraint((self.source),(self.target),mo = moV)
        return self.con
    
    def orientCon(self,moV):
        self.con = cmds.orientConstraint((self.source),(self.target),mo= moV)
        return self.con
    
    def parentCon(self,moV):
        self.con =cmds.parentConstraint((self.source),(self.target),mo = moV)
        return self.con
    
    def poleVecCon(self):
        self.con = cmds.poleVectorConstraint(self.source,self.target)
        return self.con


    def pointOriCon(self,moV):
        dtO = dt.DailyTool()        
        con = [self.pointCon(moV),self.orientCon(moV)]
        self.con = dtO.appendIt(con)        
        return self.con
    
    def makeConGrp(self,conType,name=None):
        dtO = dt.DailyTool()
        dtO.cls()
        if name == None:
            name = self.source       
            
        self.target = cmds.group(n = (name+'_g'),em =1)
        if conType == 0:
            self.pointCon(0)
        if conType == 1:
            self.orientCon(0)
        if conType == 2:
            self.pointOriCon(0)
        for i in range(0,len(self.con)):
            cmds.delete(self.con[i])
                    
        return self.target
    
    def makeOffGrp(self,conType,name=None):
        self.target = self.makeConGrp(conType,name)
        cmds.parent(self.source, self.target)
        return self.target
        


class MakeDisNode(object):
    def __init__(self,obj1,obj2=None,lenght=None,gCtrl=None):
        self.obj1  = obj1
        self.obj2 = obj2
        self.mdn = cmds.createNode('multiplyDivide',n = (self.obj1+'_divS_mdn'))
        self.mdnG = cmds.createNode('multiplyDivide',n = (self.obj1+'_GlobalS_mdn'))
        self.con = cmds.createNode('condition',n = (self.obj1+'_divS_con'))
        self.lenght = lenght
        self.gCtrl =  gCtrl
    
   
    
    def curveDisNode(self):
        disNode = cmds.arclen(self.obj1,ch=1)
        disNode = cmds.rename(disNode,(self.obj1+'_crvInfo'))
        disVal = cmds.getAttr(disNode+'.arcLength')
        cmds.connectAttr((self.mdnG+'.outputX'),(self.mdn+'.input1X'),f=1)
        self.mdnConnector((disNode+'.arcLength'), disVal)
        print self.gCtrl
        if(self.gCtrl):
            self.globalScaleConnector(self.gCtrl)
        return self.con
                     
    def LocDisNode(self):
        
        spVal = dt.getXform(self.obj1,1)
        epVal = dt.getXform(self.obj2,1)
        disNode = cmds.distanceDimension(sp = (spVal.Xval),ep = (epVal.Xval))
        disNodeparent = cmds.rename((dt.findParent(disNode).parent),(self.obj1+'_disNode'))
        disNode  = (disNodeparent+'Shape')            
        spEdLoc = cmds.listConnections(disNode,d=1)            
        spEdLoc[0] = cmds.rename(spEdLoc[0],(self.obj1+'_disLoc'))
        spEdLoc[1] = cmds.rename(spEdLoc[1],(self.obj2+'_disLoc'))
        ApplyConstrain(self.obj1,spEdLoc[0]).pointCon(0)
        ApplyConstrain(self.obj2,spEdLoc[1]).pointCon(0)
        
        Val = cmds.getAttr(disNode+'.distance')        
        #passing overall length if needed(needed for 2b,3b chain joints)        
        if self.lenght != None:
            Val =  self.lenght
        
        self.mdnConnector((disNode+'.distance'), Val)
        #cmds.connectAttr((disNode+'.distance'),(self.con+'.firstTerm'),f=1)
        cmds.connectAttr((self.mdnG+'.outputX'),(self.con+'.firstTerm'),f=1)
        cmds.connectAttr((self.mdnG+'.outputX'),(self.mdn+'.input1X'),f=1)
        cmds.setAttr(self.con+'.secondTerm',Val)
        if(self.gCtrl):
            self.globalScaleConnector(self.gCtrl)
        
        #Housekeeping 
        perG = cmds.group( em=True, name= (disNodeparent+'_g'))
        cmds.parent(spEdLoc,disNodeparent,perG)
        
        return self.con
     
    
        
    def mdnConnector(self,disAtter,Val):
        cmds.setAttr(self.mdnG+'.operation',2)
        cmds.setAttr(self.mdn+'.operation',2)
        #cmds.connectAttr((disAtter),(self.mdn+'.input1X'),f =1)
        cmds.connectAttr((disAtter),(self.mdnG+'.input1X'),f =1)
        cmds.setAttr(self.mdn+'.input2X',Val)
        cmds.setAttr(self.con+'.operation',2)
        cmds.connectAttr((self.mdn+'.outputX'),(self.con+'.colorIfTrueR'),f =1)
    
    def globalScaleConnector(self,gCtrl):
        cmds.connectAttr((gCtrl+'.RigScale'),(self.mdnG+'.input2X'),f=1)
        
        
        


        
class RelationNameHoler:
    def __init__(self,name,attrName):
        self.name = name
        self.attrName = attrName

class DriverDrivenAttrHolder:
    def __init__(self,defaultValue=None,minValue=None,maxValue=None):
        self.defaultValue = defaultValue
        self.minValue = minValue
        self.maxValue = maxValue

class AttributeHolder(RelationNameHoler,DriverDrivenAttrHolder):
    def __init__(self,name,attrName,defaultValue,minValue,maxValue):
        RelationNameHoler.__init__(self, name, attrName)
        DriverDrivenAttrHolder.__init__(self, defaultValue, minValue, maxValue)        


class AddDriverAttr(AttributeHolder):
    def __init__(self,name,attrName,defaultValue,minValue,maxValue,attrType):
        AttributeHolder.__init__(self, name, attrName, defaultValue, minValue, maxValue)
        self.attrType = attrType
        
        cmds.select(self.name)
        if self.attrType == 'float':
            cmds.addAttr(ln = self.attrName,dv = self.defaultValue,min = self.minValue,max = self.maxValue,at = self.attrType,k=1)
        elif self.attrType == 'enum':
            cmds.addAttr(ln=self.attrName,at ='enum',en = self.enum,k=1)
        elif self.attrType == 'bool':
            cmds.addAttr(ln=self.attrName,at ='bool',k=1)


class DriverDriven:
    
    def __init__(self,driven,dnAttr,dnDeValue,dnMin,dnMax,driver,drAttr,drDeValue,drMin,drMax,attrType,enum=None):
        self.driven = driven
        self.dnAttr = dnAttr
        self.dnDeValue = dnDeValue
        self.dnMin = dnMin
        self.dnMax = dnMax
        self.driver = driver
        self.drAttr = drAttr
        self.drDeValue = drDeValue
        self.drMin = drMin
        self.drMax = drMax
        self.attrType = attrType
        self.enum = enum

    
    def setDrive(self,count):
        self.driver = AddDriverAttr(self.driver,self.drAttr,self.dnDeValue,self.drMin,self.drMax,self.attrType,self.enum)
        self.driven = AttributeHolder(self.driven,self.dnAttr,self.dnDeValue,self.dnMin,self.dnMax)
        driverVal = [self.drDeValue,self.drMax,self.drMin]
        drivenVal = [self.dnDeValue,self.dnMax,self.dnMin]
                
        for i in range(0,count):
            cmds.setDrivenKeyframe((self.driven.name+'.'+self.driven.attrName),cd= (self.driver.name+'.'+self.driver.attrName),dv=(driverVal[i]),v=(drivenVal[i]))
        
    
    def ConnectAttr(self):
        self.driver = AddDriverAttr(self.driver,self.drAttr,self.dnDeValue,self.drMin,self.drMax,self.attrType,self.enum)
        self.driven = RelationNameHoler(self.driven,self.dnAttr)
        cmds.connectAttr((self.driver.name+'.'+self.driver.attrName),(self.driven.name+'.'+self.driven.attrName),f=1)



class FingerAttrHolder:
    def __init__(self,fingers,UD,LR,Twist,axis,diverVal,drivenVal):
        self.fingers = fingers
        self.UD = UD
        self.LR = LR
        self.Twist = Twist
        self.axis = axis
        self.driveAttr = [self.UD,self.LR,self.Twist]
        self.diverVal = diverVal
        self.drivenVal = drivenVal
        #self.suffix = '_jnt'
    
    def makeSetDriveFinger(self):        
        for i in range(0,len(self.fingers)):
            for j in range(0,len(self.driveAttr)):
                for k in range(0,len(self.driveAttr[j])):
                    obj = DriverDriven((self.fingers[i]+str(k+1)+self.suffix),(self.axis[j]),(self.drivenVal[0]),(self.drivenVal[1]),(self.drivenVal[2]),(self.fingers[i]),(self.driveAttr[j][k]),(self.diverVal[0]),(self.diverVal[1]),(self.diverVal[2]),'float').setDrive(3)
                    
                    

        


fingers = ['Index','middle']
UD = ['UD1','UD2','UD3']
LR = ['LR1','LR2','LR3']
Twist = ['Twist1','Twist2','Twist3']
axis = ['ry','rz','rx']
diverVal = [0,-10,10]
drivenVal = [0,-60,60]

##aa = FingerAttrHolder(fingers,UD,LR,Twist,axis,diverVal,drivenVal).makeSetDriveFinger()



class rigHouseKeeping:
    
    def __init__(self,name):
        self.name =  name
        
        
    def makeBasicGroup(self,name):
        self.grp =  cmds.group( em=True, name = name )
        cmds.select(cl=1)
        return self.grp
    
    def makeAllHouseKeepingGroup(self,skip):
        self.rigHGrp =  ['rig_g','kinematics_g','helper_g','geometry_g']        
        topG =  self.makeBasicGroup(self.name)            
            
        for i in range(0,len(self.rigHGrp)-skip):
            grp = self.makeBasicGroup(self.rigHGrp[i])
            if topG !=  None:
                dt.parentIT(grp,topG)                
                
        return self.rigHGrp
    
    def rigParent(self,rig,kinematics,helper):
        if cmds.objExists('rig_g') and cmds.objExists('kinematics_g') and cmds.objExists('helper_g') :
            for i in range(0,len(rig[0])):
                dt.parentIT((rig[0][i]),(rig[1][i]))
            for j in range(0,len(kinematics)):
                dt.parentIT((kinematics[j]),('kinematics_g'))
            for k in range(0,len(helper)):
                dt.parentIT((helper[k]),('helper_g'))
                           
        else:
            print 'Please create global group'




class JointRigInfo(object):
    def __init__(self,startJoint):
        self.startJoint = startJoint
        self.joint =  jo.JointOperation()
        dtO = dt.DailyTool()
        self.stEd = self.joint.jointsInfo(self.startJoint,0)
        self.allJnts = self.joint.jointsInfo(self.startJoint,1)
        dtO.cls()




class FkCtrlRig(JointRigInfo):
    def __init__(self,startJoint,hierarchy,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
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
        self.hierarchy =  hierarchy            
        count = 0 
        
        print self.sx ,self.sy,self.sz
        
        if self.hierarchy == 0:
            count = (len(self.allJnts)-1)
            
        print count
        
        for i in range(0,len(self.allJnts)-count):
            cmds.select(self.allJnts[i])
            co.MakeCtrl(self.allJnts[i]+'_ctrl',self.ctrlChoice,self.sx,self.sy,self.sz,self.color,1,self.allJnts[i],self.nx,self.ny,self.nz,self.redi)





        
class SpineIkRig(JointRigInfo):
    def __init__(self,startJoint,numS,ctrlName,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None,gScale =None):
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
        self.gScale =  gScale
        
       
                      
        kmo = IKSpline(self.stEd[0], self.stEd[1])
        self.ikH = kmo.applyIk(self.numS)
        crv = co.CurveOperation(self.ikH[2]) 
        self.jntCtrls = crv.curveSkinCtrls(0,self.ctrlName)        
        
        for i in range(0,len(self.jntCtrls)):            
            kmg = ApplyConstrain(self.jntCtrls[i])
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
        
        
        #connectAttr -f Placer.RigScale spine01_crv_GlobalS_mdn.input2X;
        
        
        con = MakeDisNode(self.ikH[2],None,6,self.gScale).curveDisNode()
        print con 
        print self.gScale
        cmds.connectAttr((comShape+'.stretchy'),(con+'.firstTerm'))
        conAttr = con+'.outColorR'        
        jo.jointScale(self.allJnts,'sx',conAttr)       
        
        twisterJnt = [self.jntCtrls[0],self.jntCtrls[-1]]
        twistJnt = [self.stEd[0],self.stEd[1]]
        
        for i in range(0,2):
            grp = cmds.group(em =1, n =(twistJnt[i]+'Twist_g'))
            delCon = ApplyConstrain(twistJnt[i],grp).pointOriCon(0)
            cmds.delete(delCon[0],delCon[1])
            cmds.parent(grp,twisterJnt[i])
        
        cmds.setAttr(self.ikH[0]+'.dTwistControlEnable',1)
        cmds.setAttr(self.ikH[0]+'.dWorldUpType',4)
        cmds.connectAttr((twistJnt[0]+'Twist_g.worldMatrix[0]'),(self.ikH[0]+'.dWorldUpMatrix'),f=1)
        cmds.connectAttr((twistJnt[1]+'Twist_g.worldMatrix[0]'),(self.ikH[0]+'.dWorldUpMatrixEnd'),f=1)
        






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
            self.bipCtrlsG.append(ApplyConstrain(self.bipCtrls[i]).makeOffGrp(2))
        
        
        self.bipCtrlsG.extend(spineInctrlG)        
        for i in range(0,len(self.bipCtrlsG)-1):
            cmds.parent(self.bipCtrlsG[i+1],self.bipCtrls[parentOrder[i]])
            
        hipRefPiv = ApplyConstrain(self.jntCtrls[1]).makeConGrp(2,'hipPiv')
        torsoRefPiv = ApplyConstrain(self.jntCtrls[1]).makeConGrp(2,'torsoPiv')
        ApplyConstrain(hipRefPiv,self.bipCtrlsG[-1]).parentCon(1)
        ApplyConstrain(torsoRefPiv,self.bipCtrlsG[-1]).parentCon(1)
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
        self.bipCtrlsG.append(ApplyConstrain(self.bipCtrls[-1]).makeOffGrp(2))
        dt.parentIT(self.bipCtrlsG[5],self.bipCtrls[2])
        dt.parentIT(self.bipCtrlsG[3],self.bipCtrls[5])
        
    




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
        self.topG =  ApplyConstrain(self.startJont).makeOffGrp(2,(self.startJont+'Rig'))
        
        # making IkHendle Ctrl
        self.ikHJnt =  jo.JointOperation().makeDuplicateJointChaines(self.sourceJnt[2],self.sourceJnt[2],'_Ikctrl')
        
        #adding attributes 
        cmds.select(self.ikHJnt[0])
        AddDriverAttr(self.ikHJnt[0],'upperLimb',0,-10,10,'float')
        AddDriverAttr(self.ikHJnt[0],'lowerLimb',0,-10,10,'float')
        cmds.addAttr(ln= 'ikFK',at = 'enum',en = 'Ik:fk',k=1)
        AddDriverAttr(self.ikHJnt[0],'stretchy',None,None,None,'bool')
            
        co.MakeCtrl(self.ikHJnt[0]+'_ctrl',2,0.5,0.5,0.5,ctrlColor,1,self.ikHJnt[0])
        self.ikHJntG = ApplyConstrain(self.ikHJnt[0]).makeOffGrp(2)
        
               
        #make ikFk Chain and connect it to ikHandle
        self.ikJnt =  jo.JointOperation().makeDuplicateJointChaines(self.startJont,self.startJont, '_ik')
        self.ikJntG = ApplyConstrain(self.ikJnt[0]).makeOffGrp(2)
        self.fkJnt = jo.JointOperation().makeDuplicateJointChaines(self.startJont,self.startJont, '_fk')
        self.fkJntG = ApplyConstrain(self.fkJnt[0]).makeOffGrp(2)
        cmds.parent(self.ikJntG,self.topG)
        cmds.parent(self.fkJntG,self.topG)
        
        self.rev =  cmds.createNode('reverse',n = (self.startJont+'ikFk_rev'))
        cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.rev+'.inputX'))
                 
        for i in range(0,len(self.sourceJnt)):
            self.ikCon = ApplyConstrain(self.ikJnt[i],self.sourceJnt[i]).parentCon(0)
            self.fkCon = ApplyConstrain(self.fkJnt[i],self.sourceJnt[i]).parentCon(0)
            conW =  cmds.parentConstraint(self.ikCon,q=1 ,wal=1)
            cmds.connectAttr((self.rev+'.outputX'),(self.ikCon[0]+'.'+conW[0]))
            cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.ikCon[0]+'.'+conW[1]))
               
        #make FK rig
        
        FkCtrlRig(self.fkJnt[0],1,1,1,1,1,self.ctrlColor,1,0,0,2)
        cmds.connectAttr((self.ikHJnt[0]+'.ikFK'),(self.fkJntG+'.visibility'))
                   
        
        ApplyConstrain(self.ikHJnt[0], self.ikJnt[2]).orientCon(0)        
        co.MakeCtrl(self.poleCtrl+'_ctrl',2,0.5,0.5,0.5,ctrlColor,1,self.poleCtrl)
        self.refLine = co.MakeCtrl(self.ikJnt[1]+'Ref_ctrl',6,1,1,1,13,startConCtrl=self.ikJnt[1],endConCtrl=self.poleCtrl)
       
          
          
            
        self.ikH =  twoJointIk(self.ikJnt[0],2,self.poleCtrl)
        cmds.parent(self.ikH.ikH[0],self.ikHJnt[0])
        self.poleCtrlG = ApplyConstrain(self.poleCtrl).makeOffGrp(2)
        ApplyConstrain(self.ikJntG,self.poleCtrlG ).pointCon(1)
        ApplyConstrain(self.ikHJnt[0],self.poleCtrlG ).pointCon(1)
        cmds.connectAttr((self.rev+'.outputX'),(self.ikJntG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.ikHJntG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.poleCtrlG+'.visibility'))
        cmds.connectAttr((self.rev+'.outputX'),(self.refLine.name+'.visibility'))
        

        #make fkJoint stretchy makeStetchyFK(self,attrName,scaleAxies)
        makeStretchy(self.fkJnt[0]).makeStetchyFK('stretch','scaleX')
        makeStretchy(self.ikJnt[0],self.gCtrl).makeStretchyIK(self.ikHJnt[0],2)
       
        
        #Housekeeping Groups
        rigCG = [self.topG,self.ikHJntG,self.poleCtrlG]
        rigPG = [self.rigParent,self.rigParent,self.rigParent]
        rigG = [rigCG,rigPG]
        kinematicsG = [(self.ikJntG+'_disNode_g'),self.refLine.hkG]
        helperG = [self.refLine.ctrl]
        rigHouseKeeping(self.rigName).rigParent(rigG, kinematicsG, helperG)
        #cmds.setAttr((self.ikH.ikH[0]+'.visibility'),0)

       


#aa = makeTwoJointIkFkRig('L_2bIkFK_','L_Shoulder','L_ArmPole',13,'mover2',gCtrl='Placer')

  
class feetRig():
    
    def makeFeetRig(self,startJoint,Ctrl,ikH,atrrs,refPiv1,refPiv2):
        self.sourceJnt  =  jo.JointOperation().jointsInfo(startJoint,1)
        
        ikHBall =  twoJointIk(self.sourceJnt[0],1)
        ikHToe =  twoJointIk(self.sourceJnt[1],1)      
        
        sdkPivG = [self.sourceJnt[1],self.sourceJnt[1],refPiv1,refPiv2]
        
        self.parentSDKG = []
        self.drivens =  []
        for i in range(0,len(atrrs)):
            self.drivens.append(ApplyConstrain(sdkPivG[i]).makeConGrp(0, atrrs[i]))
            self.parentSDKG.append(ApplyConstrain(self.drivens[i]).makeOffGrp(2, self.drivens[i]))
            
        for i in range(0,len(self.parentSDKG)-1):
            if(i == 2):
                pIndex = 3
            else:
                pIndex =  2                
            dt.parentIT(self.parentSDKG[i],self.parentSDKG[pIndex][:-2])           
        
        dt.parentIT(ikH,self.drivens[0])
        dt.parentIT(ikHBall.ikH[0],self.drivens[0])
        dt.parentIT(ikHToe.ikH[0],self.drivens[1])
        dt.parentIT(self.parentSDKG[-1],Ctrl)
        
                
        axis = 'rx'
        driverVal = [[0,0,10],[0,-10,10],[0,0,10],[0,0,10]]
        drivenVal =[[0,0,90],[0,90,-90],[0,0,90],[0,0,-90]]
        
        for i in range(0,len(self.drivens)):
            AddDriverAttr(Ctrl,atrrs[i],driverVal[i][0],driverVal[i][1],driverVal[i][2],'float')                         
            for j in range(0,3):
                cmds.setDrivenKeyframe((self.drivens[i]+'.'+axis),cd= (Ctrl+'.'+atrrs[i]),dv=(driverVal[i][j]),v=(drivenVal[i][j]))
        
        
  
    
class makeTwoJointIkFkLegRig(makeTwoJointIkFkRig):
    def __init__(self,rigName,startJoint,poleCtrl,ctrlColor,rigParent,toeTipPivot,heelPivot, gCtrl=None):
        makeTwoJointIkFkRig.__init__(self, rigName, startJoint, poleCtrl, ctrlColor, rigParent, gCtrl)
        self.toeTipPivot =  toeTipPivot
        self.heelPivot =  heelPivot

        #clean up Extra ikCtrls and addtional shape on toeTip
        for i in range(1,len(self.ikHJnt)-1):
            cmds.delete(self.ikHJnt[i])
        
        cmds.delete(co.Curve(self.fkJnt[-1]).curve)        
        Attrs = ['toeRoll','toeTap','frontRoll','heelRoll']  
        
        feetRig().makeFeetRig(self.ikJnt[2],self.ikHJnt[0],self.ikH.ikH[0],Attrs,self.toeTipPivot,self.heelPivot)


class neckRig(SpineIkRig):
    def __init__(self,startJoint,numS,ctrlName,ctrlChoice,sx,sy,sz,color,nx=None,ny=None,nz=None,redi=None):
        SpineIkRig.__init__(self, startJoint, numS, ctrlName, ctrlChoice, sx, sy, sz, color, nx, ny, nz, redi)
