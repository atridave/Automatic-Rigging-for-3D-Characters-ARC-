import maya.cmds as cmds
import DailyTool as dt
import kinematics as km
import math



class JointOperation:
    
    def makeJnt(self,name):
        self.jnt =  cmds.joint(p=(0,0,0),n= name)
        return self.jnt
    
    def jointsInfo(self,joint,allJnt):
        self.stEd = []
        jnt = dt.DailyTool()
        jnt.sl(joint)
        jnt.sHI(joint)
        self.allJoints = cmds.ls(sl =1,typ = 'joint')
        self.stEd.append(self.allJoints[0])
        self.stEd.append(self.allJoints[-1])
        
        if allJnt == 1:
            return self.allJoints
        else:
            return self.stEd
        
    def jointDisInfo(self,parentJnt,childJnt):
        parent =  cmds.xform(parentJnt,q=1,t=1,ws =1)
        child = cmds.xform(childJnt,q=1,t=1,ws =1)
        self.dis = math.sqrt( (child[0]-parent[0])*(child[0]-parent[0])+ (child[1]-parent[1])*(child[1]-parent[1])+ (child[2]-parent[2])*(child[2]-parent[2]))
        return self.dis
    
    def jointLengthInfo(self,joint,jntCount = None):
        length = 0
        self.jntCount = jntCount
        jntChain = self.jointsInfo(joint,1)
        
        if (self.jntCount == None):
            self.jntCount  = len(jntChain)   
        
        for i in range(0,self.jntCount):
            dis = self.jointDisInfo(jntChain[i], jntChain[i+1])
            length += dis
        return length
                   
        

    def jointRecreate(self,joint):
        prifix = 'new_'
        cmds.select(cl=1)
        self.newJnt  =  self.makeJnt(prifix+joint)
        print joint,self.newJnt
        aa =  km.ApplyConstrain(joint,self.newJnt).pointOriCon(0)
        cmds.delete(aa[0],aa[1])
        cmds.makeIdentity( apply=True, t=1, r=1, s=1)        
        print 'I am recreating all joints'        
        
        
    def creatCtrlJoints(self,xval,yval,zval):
        self.jnt = cmds.joint(p=(xval,yval,zval))
        return self.jnt
    
    def makeDuplicateJointChaines(self,SourceJoint,name,suffix):
        dJoints =  []
        joints =  cmds.duplicate(SourceJoint,n = (name+suffix),rc=1)
        dJoints.append(joints[0])
        for i in range(1,len(joints)):
            nameName =  (joints[i].strip((joints[i][-1])))
            newJntName = cmds.rename(joints[i],(nameName+suffix))
            dJoints.append(newJntName)
        return dJoints       




class jointScale:
    def __init__(self,joints,axies,conAttr):
        self.conAttr = conAttr
        self.axies = axies
        self.joints  = joints        
        for i in range(0,len(self.joints)):
            cmds.connectAttr((self.conAttr),(self.joints[i]+'.'+self.axies),f=1)
            


        
             
        



