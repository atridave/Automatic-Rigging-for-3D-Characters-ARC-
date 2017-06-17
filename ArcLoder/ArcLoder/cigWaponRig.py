'''
Created on 10 Feb 2016

@author: adave
'''
import sys
import maya.cmds  as cmds
import jointOperation as jo
import kinematics  as km
import CurveOperation as co
import spineRig as spr
import DailyTool as dt
import Red9.core.Red9_Meta as r9Meta
import Red9_ClientCore.CloudImp.metadata as cigmeta

reload(co)
reload(jo)
reload(km)
reload(spr)
reload(dt)



class weponRig:
    
    def __init__(self):
        pass
    
    def loadWeaponSkelaton(self):
        pass 
    
    def getObj(self):
        self.sel = cmds.ls(sl=1)
        
        return self.sel
    
    def makeBasicGroup(self,name):
        self.name  =  name
        self.grp =  cmds.group( em=True, name= (self.name) )
        cmds.select(cl=1)
        return self.grp
    
    
        
    def makeAllBasicGroup(self,itemname):
        self.itemName = itemname  
        self.itemGrp = self.makeBasicGroup(itemname)
        self.SceneRoot = self.makeBasicGroup('SceneRoot')
        self.makeEngineReady(self.SceneRoot,(90,0,180))
        
        self.grps = ['rig','geometry','export','cgf','skin','CHR','oldMeshRef']
        self.phyGrp = []
        for i in range(0,len(self.grps)):            
            self.phyGrp.append(self.makeBasicGroup(self.grps[i]+'_g'))   
       
        cmds.parent(self.phyGrp[0],self.itemGrp)
        cmds.parent(self.phyGrp[1],self.itemGrp)
        cmds.parent(self.phyGrp[2],self.phyGrp[1])
        cmds.parent(self.phyGrp[3],self.phyGrp[2])
        cmds.parent(self.phyGrp[4],self.phyGrp[2])
        cmds.parent(self.phyGrp[5],self.phyGrp[2])
        cmds.parent(self.phyGrp[6],self.phyGrp[2])
        
        
                 
    def makeJnt(self,name,parent):
        self.name = name
        value =  [90,0,180]
        cmds.select(cl=1)        
        self.Jnt =  cmds.joint(n = self.name)
        self.makeEngineReady(self.Jnt,value)
        cmds.makeIdentity( self.Jnt,apply=True )
        cmds.parent(self.Jnt,parent)
        if self.name == 'camera':
            weponRig().makeCamera(self.name)
            
            
            
            
    def makeAllJnts(self,joints):
        self.joints =  joints 
        for i in range(len(self.joints)):
            if i == 0:
                self.makeJnt(self.joints[i],'SceneRoot')
            else:
                self.makeJnt(self.joints[i], self.joints[0])
            
        
        

    def makeEngineReady(self,obj,value):
        self.obj =  obj
        self.value =  value
        rotateAxies =  ['.rx','.ry','.rz']
               
        for i in range(len(self.value)):
            cmds.setAttr((self.obj+rotateAxies[i]),self.value[i])
        ##Add camera too 
        
        
    def makeCamera(self,parent):
        self.camera = cmds.camera(hfa = (1.417),vfa = (0.945),focalLength = (35),lensSqueezeRatio = (1),fStop = (5.6),focusDistance = (200),shutterAngle = (144),centerOfInterest = (200))
        self.camera = cmds.rename(self.camera[0],'weaponCamera')
        self.con = km.ApplyConstrain(parent,self.camera).pointOriCon(0)
        cmds.delete(self.con[0],self.con[1])      
        cmds.parent(self.camera,parent)
        self.makeEngineReady(self.camera,(90,0,0))
        
    def makeRefPoints(self,obj):
            
        grp =  cmds.group(em=1,n = 'refpoint_g')
        for i in range(len(obj)):
            cmds.select(cl=1)
            loc = cmds.spaceLocator(n=obj[i]+'_loc')
            cmds.parent(loc,grp)
        



        
    def makeRig(self):
        self.sel = cmds.ls(sl=1)
        rigCtrls = []
        if self.sel:
            for i in range(len(self.sel)):
                cmds.select(cl=1)
                self.parent = cmds.listRelatives(self.sel[i],p=1)
                self.joint = jo.JointOperation().makeJnt(self.sel[i]+'_Ctr')                
                print self.parent
                self.jntG = km.ApplyConstrain(self.joint).makeOffGrp(2)
                self.con =  km.ApplyConstrain(self.sel[i],self.jntG).pointOriCon(0)
                cmds.delete(self.con[0],self.con[1])
                if(self.parent[0] != None ) and (self.parent[0] != 'SceneRoot' ):
                    print self.jntG,self.parent[0]
                    cmds.parent(self.jntG,(self.parent[0]+'_Ctr'))                    
                self.con =  km.ApplyConstrain( self.joint,self.sel[i]).pointOriCon(0)
                dt.LockHide(self.jntG,1,1,1,1,1,1,1,1,1,1)                
                            
                if self.sel[i] == 'root':
                    spr.FkCtrlRig(self.joint,2,5,15,15,17)                                 
                else:
                    spr.FkCtrlRig(self.joint,2,3,3,3,13)                   
                
                dt.LockHide(self.joint,0,0,0,0,0,0,1,1,1,1,1)
                dt.DailyTool().appendIt(self.joint)
                cmds.select(self.joint)
        else:
            sys.stdout.write('give me some node to work')
        return rigCtrls
        
    def red9Addon(self,nameofmrig,rootCtrl):
        mrig=r9Meta.getMetaNodes('Pro_MetaRig_Prop')
        if mrig:
            r9Meta.convertMClassType(mrig[0], cigmeta.CIG_Pro_MetaRig_Prop)
            tag=r9Meta.getMetaNodes('ExportTag_Prop')
            if tag:
                r9Meta.convertMClassType(tag[0], cigmeta.CIG_ExportTag_Prop)
    
    
        nameofmrig=nameofmrig
        tagID='ExportTag_Prop'
        main_ctrl=rootCtrl  # main controller for the weapon to wire up to the mrig
        skeletonroot='root'  # joit thats the root of the skeleton'
        mrig=cigmeta.CIG_Pro_MetaRig_Prop(name=nameofmrig)
        mrig.addMainCtrl(main_ctrl)
        mrig.addExportTag(tagID=nameofmrig,exportClass=cigmeta.CIG_ExportTag_Prop)
        mrig.exportTag.exportRoot=skeletonroot
        mrig.attachnode=main_ctrl
        #setAttr should come for changing tagID and ExportRoot
        
    def gameFileEdtiting(self):
        pass
        # skelation Edting file Path :: //starcitizen/game-dev/CryEngine/Data/Animations/SkeletonList.xml
        #database Edting path :: //starcitizen/game-dev/CryEngine/Data/Animations/DBATable.json
        #entity update :: 
    
    def makePhysSetup(self):
        self.parentFPhyLoc =  cmds.spaceLocator(n=('root_PhysParentFrame'))
        self.phyLoc =  cmds.spaceLocator(n=('root_Phys'))
        self.makeEngineReady(self.parentFPhyLoc[0],(90,0,180))
        self.makeEngineReady(self.phyLoc[0],(90,0,180))        
        cmds.parent(self.phyLoc[0],self.parentFPhyLoc[0])
        cmds.parent(self.parentFPhyLoc,'rig_g')
        dt.LockHide(self.parentFPhyLoc[0],0,0,0,0,0,0,0,0,0,0)
        phyGeo =  cmds.polyCube(n='root_PhysGeo',w=10,h=20,d=50,ch=0)
        cmds.parent(phyGeo[0],'root')
        cmds.makeIdentity(phyGeo[0],apply=True )        
        cmds.addAttr('root_Ctr',ln='proxy',at = 'enum', en= ('Off:On'),k=1)
        cmds.connectAttr('root_Ctr.proxy',(phyGeo[0]+".visibility"), f=1)
        phyGeo = cmds.rename(phyGeo,'root_Phys')
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
   

    
     



#print aa


#aa = weponRig().makeAllBasicGroup('bsgn_fps_ksar_ravager')

#joints = ['root','camera','weapon_term','trigger','magAttach','safe','bolt','magrelease','L_barrel','charging','pump']
#joints = ['root']
#refLoc = weponRig().makeRefPoints(joints)

#ab = weponRig().makeAllJnts(joints)
#ab = weponRig().makeRig()

#aa =  weponRig().makePhysSetup()


#ab = weponRig().red9Addon('brfl_behr_p8ar', 'root_Ctr')


#aa=  weponRig().makePhysSetup()

