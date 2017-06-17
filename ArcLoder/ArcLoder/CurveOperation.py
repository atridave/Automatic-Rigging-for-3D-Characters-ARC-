import maya.mel as mel
import maya.cmds as cmds
import DailyTool as dt
import jointOperation as jo
import kinematics as km

class CurveOperation:
    
    def __init__(self,curve):
        self.curve = curve
    
    def curveCvInfo(self):
        cvInfo = []
        Degree = cmds.getAttr(self.curve+'.degree')
        Spans =  cmds.getAttr(self.curve+'.spans')
        Cvs = Degree+Spans
        cvInfo.append(Degree)       
        cvInfo.append(Cvs)
        return cvInfo
        
    def convertToBezier(self):
        dtO = dt.DailyTool()
        dtO.sl(self.curve)
        cmds.nurbsCurveToBezier()
        dtO.delHis(self.curve)
        
    def curveSkinCtrls(self,allc,name):
        
        self.ctrlJnts = []
        dtO = dt.DailyTool()
        Crv = self.curveCvInfo()
        joO = jo.JointOperation()        
        dtO.delHis(self.curve)
                       
        for i in range(0,Crv[1]):
            dtO.cls()
            jntPV = cmds.getAttr(self.curve+'.cv[%d]' % i)
            jntP = jntPV[0]
            jnt = joO.creatCtrlJoints(jntP[0],jntP[1],jntP[2])
            self.ctrlJnts.append(jnt)
            dtO.cls()
        if allc == 0:
            cmds.delete(self.ctrlJnts[1])
            cmds.delete(self.ctrlJnts[(Crv[1]-2)])
            self.ctrlJnts.pop(1)
            self.ctrlJnts.pop(-2)
        cmds.select(self.ctrlJnts)
        sel = cmds.ls(sl=1)
        for i in range(0,len(sel)):
            a = i+1
            reJnt =cmds.rename((sel[i]),((name+'0%d') % a ) )
            self.ctrlJnts.pop(0)
            self.ctrlJnts.append(reJnt)
        cmds.select(self.ctrlJnts,self.curve)
        cmds.skinCluster(n = name+'_skin')
        
        return self.ctrlJnts
    
        
         
class Curve(object):
    def __init__(self,curve):
        self.curve = curve
        
class ShapeScaler(Curve):
    def __init__(self,curve,sx,sy,sz):
        Curve.__init__(self, curve)
        self.sx = sx
        self.sy = sy
        self.sz = sz
        cmds.select(self.curve)
        cmds.scale(self.sx,self.sy,self.sz)
        cmds.makeIdentity( apply=True, t=1, r=1, s=1)

class ShapeFinder(Curve):
    def __init__(self,curve):
        Curve.__init__(self,curve)
        self.shape = cmds.listRelatives(self.curve)
        

class ShapeRenamer(ShapeFinder):
    def __init__(self,curve,spName):
        ShapeFinder.__init__(self, curve)
        self.spName = spName
        self.shape = cmds.rename(self.shape,(self.spName+'Shape'))
        
        
class ShapeColor(ShapeRenamer):
    def __init__(self,curve,spName,color):
        ShapeRenamer.__init__(self,curve,spName)
        self.color = color
        cmds.setAttr(self.shape+'.overrideEnabled',1)
        cmds.setAttr(self.shape+'.overrideColor',color)
        
        
        
        
class ShapeDesigner(ShapeColor):
    def __init__(self,curve,spName,color):
        ShapeColor.__init__(self,curve,spName,color)
        cmds.select(self.curve)
        cmds.makeIdentity( apply=True, t=1, r=1, s=1)
        cmds.delete(self.curve,ch =1)
        
        
    def shapeParent(self,ctrlJnt):
        self.ctrlJnt = self.spName
        cmds.parent(self.shape,self.ctrlJnt,r=1,s=1)
        cmds.delete(self.curve)


 



class CtrlLib(object):
    def __init__(self,name):
        self.name = name
        
    def addShapeCurve(self):
        self.ctrl = cmds.curve(d=3,p=[(0,0,0)],k = [0,0,0], n = (self.name))
        
    def makeRefLine(self,stCtrl,edCtrl):
        self.ctrl = cmds.curve(d=1,p=[(0,0,0),(0,0,12)],k = [0,1], n = (self.name))
        self.stCtrl =  stCtrl
        self.edCtrl =  edCtrl
        cmds.select(self.ctrl+'.cv[0]')
        stClu = cmds.cluster(n=(self.ctrl+'st_clu'))
        cmds.select(self.ctrl+'.cv[1]')
        edClu = cmds.cluster(n=(self.ctrl+'ed_clu'))
        km.ApplyConstrain(self.stCtrl,stClu).parentCon(0)
        km.ApplyConstrain(self.edCtrl,edClu).parentCon(0)
        cmds.setAttr(self.ctrl+'.overrideEnabled', 1)
        cmds.setAttr(self.ctrl+'.overrideDisplayType', 2)
        self.hkG = cmds.group(n = (stClu[1]+'_g'),em =1)
        dt.parentIT(stClu[1],self.hkG)
        dt.parentIT(edClu[1],self.hkG)
        return self.hkG
            
    def makeCube(self):
        self.ctrl =  cmds.curve(d = 1, p = [((1), (1), (1)), ((1), (1), -(1)), (-(1), (1) ,-(1)), (-(1), -(1), -(1)) , ((1), -(1) ,-(1)) , ((1), (1), -(1)) , (-(1), (1), -(1)) , (-(1), (1), (1)) , ((1), (1), (1)) , ((1), -(1), (1)) , ((1) ,-(1), -(1)) , (-(1), -(1) ,-(1)) , (-(1), -(1), (1)) , ((1), -(1), (1)) , (-(1), -(1), (1)) , (-(1), (1) ,(1))],k = [ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 ], n = (self.name))
        return self.ctrl
    
    def makeCircle(self,nx,ny,nz,redi):
        self.ctrl = cmds.circle(nr = (nx,ny,nz),r=redi,ch=0, n = (self.name))
        self.ctrl = self.ctrl[0]
        return self.ctrl
    
    
    def addDummyShape(self):
        self.ctrl = cmds.curve(d=3,p=[(0,0,0)],k = [0,0,0],n=(self.name))
        return self.ctrl
    
    def makeFourArrow(self):
        self.ctrl = cmds.curve(d=1,p = [(0, 0 ,-1.98) ,(-0.495, 0, -1.32) ,(-0.165 ,0 ,-1.32) ,(-0.165, 0 ,-0.165) ,(-1.32, 0 ,-0.165) ,(-1.32, 0, -0.495) ,(-1.98, 0, 0) ,(-1.32, 0 ,0.495) ,(-1.32, 0, 0.165) ,(-0.165, 0, 0.165) ,(-0.165, 0, 1.32) ,(-0.495, 0, 1.32) ,(0, 0, 1.98) ,(0.495, 0, 1.32) ,(0.165, 0, 1.32) ,(0.165, 0 ,0.165) ,(1.32, 0, 0.165) ,(1.32, 0, 0.495) ,(1.98, 0, 0) ,(1.32, 0 ,-0.495) ,(1.32, 0 ,-0.165) ,(0.165, 0 ,-0.165) ,(0.165, 0 ,-1.32) ,(0.495, 0 ,-1.32) ,(0, 0 ,-1.98)],k = [ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24], n = (self.name)  )
        return self.ctrl
    
    def makeHip(self,nx,ny,nz,redi):
        self.ctrl = cmds.circle(nr = (nx,ny,nz),r=redi,ch=1, n = (self.name),s=12)
        self.ctrl = self.ctrl[0] 
        cmds.select(cl=1)     
        for i in range(0,12,2):
            cmds.select((self.ctrl+'.cv[%d]')%i,tgl =1)
        cmds.scale(2,2,2)
                    
        return self.ctrl
        
    def makeCog(self):
        self.ctrl = self.makeCube()
        ShapeScaler(self.ctrl,1,0.25,1)
        cmds.select(self.ctrl+'.cv[0:2]',self.ctrl+'.cv[5:8]',self.ctrl+'.cv[15]' )
        cmds.scale(.8,.8,.8)
        
    def makeHead(self):
        self.ctrl = self.makeCube()
        ShapeScaler(self.ctrl,2,1,1)
        cmds.select(self.ctrl+'.cv[0:1]',self.ctrl+'.cv[4:5]',self.ctrl+'.cv[8:10]',self.ctrl+'.cv[13]')
        cmds.scale(1.25,1.25,1.25)
        cmds.select(self.ctrl+'.cv[2:3]',self.ctrl+'.cv[6:7]',self.ctrl+'.cv[11:12]',self.ctrl+'.cv[14:15]')
        #cmds.move(0,2,0 , r =1 )
       
        


class MakeCtrl(CtrlLib):
    def __init__(self,name,choice,sx,sy,sz,color,sp =None,spJnt = None,nx=None,ny=None,nz=None,redi=None,startConCtrl=None,endConCtrl=None):
        CtrlLib.__init__(self, name)
        self.choice = choice
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.color = color
        self.sp = sp
        self.spJnt = spJnt
        self.startConCtrl = startConCtrl
        self.endConCtrl =  endConCtrl
        
        
        
        if self.choice == 0:
            self.addShapeCurve()
           
        if self.choice == 2:
            self.makeCube()
            
        if self.choice == 1:
            self.makeCircle(nx, ny, nz, redi)
        
        if self.choice == 3:
            self.makeFourArrow()
        
        if self.choice ==4:
            self.makeHip(nx, ny, nz, redi)
        
        if self.choice ==5:
            self.makeCog()
        
        if self.choice == 6:
            self.makeRefLine(self.startConCtrl, self.endConCtrl)
        
        if self.choice ==7:
            self.makeHead()
        
        

        if self.choice != 6:
            ShapeScaler(self.name,self.sx,self.sy,self.sz)
            ShapeDesigner(self.name,self.name,self.color)
        
        if self.sp :
            ShapeDesigner(self.name,self.spJnt,self.color).shapeParent(self.spJnt)
        
      







