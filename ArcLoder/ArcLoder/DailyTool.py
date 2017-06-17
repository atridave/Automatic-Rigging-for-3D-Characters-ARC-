import maya.cmds as cmds

class DailyTool:
    
    def cls(self):
        cmds.select(cl =1)
        
    def sl(self,sel):
        cmds.select(sel)
    
    def sHI(self,selected):
        self.sl(selected)
        cmds.select(hi =1)
        self.selHi = cmds.ls(sl =1)
        return self.selHi
        
    def delHis(self,sel):
        cmds.delete(sel,ch = 1) 
        
        
    def delShape(self,sel):
        cmds.delete(sel,s =1)
    
    def appendIt(self,taret):
        self.temp = []
        for i in range(0,len(taret)):
            self.temp.append(taret[i])
        return self.temp
    

            
            
            
class parentIT:
    def __init__(self,child,parent):
        self.child = child
        self.parent = parent
        cmds.parent(self.child,self.parent)
                
    

class getXform:
    def __init__(self,obj,pos=None,rot=None):
        self.Xval = []
        self.obj= obj
        self.pos = pos
        self.rot = rot
        if self.pos is not None and self.rot is None:
            self.Xval = cmds.xform(self.obj,t=1,ws=1,q=1)
        if self.rot is not None and self.pos is None:
            self.Xval = cmds.xform(self.obj,ro=1,ws=1,q=1)        
        if self.pos and self.rot is not None:
            posVal = cmds.xform(self.obj,t=1,ws=1,q=1)
            rotVal = cmds.xform(self.obj,ro=1,ws=1,q=1)
            self.Xval.append(posVal)
            self.Xval.append(rotVal)
        
       
            
class Renamer:
    def __init__(self,name,newName):
        self.name = name
        self.newName = newName
        self.name = cmds.rename(self.name,self.newName)
        
        
class findParent:
    def __init__(self,child):
        self.child = child
        self.parent = cmds.listRelatives(self.child,p =1)
        
   
class LockHide:
    def __init__(self,obj,tx,ty,tz,rx,ry,rz,sx,sy,sz,v,radi = None):
        self.obj = obj
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.v = v
        self.radi = radi
        
        self.attrs = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
        self.attrVal = [self.tx,self.ty,self.tz,self.rx,self.ry,self.rz,self.sx,self.sy,self.sz,self.v]
              
        for i in range(0,len(self.attrs)):
            if self.attrVal[i] == 1:
                key = 0
            else :
                key = 1
            cmds.setAttr((self.obj+self.attrs[i]),l=self.attrVal[i],k=key)
        
        if self.radi:
            cmds.setAttr(self.obj+'.radi', l=0,k=1)
            cmds.setAttr(self.obj+'.radi', l=1,k=0)
            


                
    

        
    
    





        