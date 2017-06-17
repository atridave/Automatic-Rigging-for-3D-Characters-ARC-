# import maya.cmds as cmds
# import kinematics as km
# import jointOperation as jo
# import DailyTool as dt
# import CurveOperation as co
# import maya.mel as mel
# reload(km)
# reload(jo)
# reload(dt)
# reload(co)
# 
# import math


import sys 
path =  sys.path

for i in range(0,len(path)):
    print path[i]

# x =  (1,1,1)
# y = (2,2,2)
# 
# 
# aa =  math.sqrt(( ( y[0]-x[0]  )*( y[0]-x[0]  )  )+(( y[1]-x[1]  )*(y[1]-x[1]   )     )+(( y[2]-x[2]  )*( y[2]-x[2]  )     ))
# 
# print aa


# import maya.standalone
# maya.standalone.initialize()

# sel = cmds.ls(sl=1)
# for i in range(0,len(sel)):
#     objName = sel[i].split("_")
#     print sel[i]
#     print objName[0]
#     aa =  km.ApplyConstrain((sel[i]),(objName[0]).pointOriCon(0)
                            
    

 
#aa =  km.ApplyConstrain('CustomAim_Ctr','CustomAim').parentCon(0)
 
 
# nameSpace =  'bhm_skeletonRed9_SRC:'
# sel =  cmds.ls(sl=1)
# selAd =  cmds.listRelatives(ad=1)
# for i in range(0,len(selAd)):
#     if cmds.nodeType(selAd[i]) == 'joint' and cmds.objExists(nameSpace+(selAd[i])) :
#         aa =  km.ApplyConstrain((selAd[i]),(nameSpace+selAd[i])).parentCon(1)
 
 
  
# sel = cmds.ls(sl=1)
# # for i in range(0,len(sel)):
# #     km.ApplyConstrain(sel[i]).makeOffGrp(2)
# 
# 
# for i in range(0,len(sel)):
#     print sel[i]
#     dt.LockHide(sel[i],0,0,0,0,0,0,0,0,0,0)
#   
#  
 
# def deleteTweak():
#     sel =  cmds.ls(type = 'tweak' )
#     if sel is not 0 :
#         cmds.delete(sel)
#     else :
#         print 'Everything is clean'
#  
# deleteTweak()
# sel = cmds.ls(sl=1)
# for i in range(0,len(sel)):
#     if cmds.nodeType( sel[i]):
#         dt.LockHide(sel[i],0,0,0,0,0,0,0,0,0,0)


# sel = cmds.ls(sl=1)
# for i in range(0,len(sel)):
#     jo.JointOperation().jointRecreate(sel[i])

# _fileName  =  cmds.file( q=True, sn=1)
# _fbxFileName =  _fileName.replace('.ma','.fbx')
# print _fbxFileName
#  
# import pymel.core as pm
# def fn():
#     importDir = _fbxFileName
#     pm.mel.FBXRead(f=_fbxFileName)
#     takes = pm.mel.FBXGetTakeCount()
#     frames = pm.mel.FBXGetTakeLocalTimeSpan(1)
# 
#     for i in xrange(1, takes + 1):
#         print(pm.mel.FBXGetTakeName(i))
#     print frames[0],frames[1]
#         
# fn()

# import maya.standalone
# maya.standalone.initialize()
# import maya.cmds as cmds
# cmds.polyCube()


#pip install p4python #installing p4python 

# pivMasterObj = 'ctrlmain_jnt_ctr_piv'
# pivChildObj =  'ctrlmain_jnt_ctr'
# attr =  '.Edit'
# con =  'ctrlmain_jnt_ctr_g_pointConstraint1.ctrlmain_jnt_ctr_pivW0'
# 
# value =  cmds.getAttr(pivMasterObj+attr)
# tMaster =  cmds.xform(pivMasterObj,q=1,t=1)
# rMaster =  cmds.xform(pivMasterObj,q=1,t=1)
# tchildVec = cmds.xform(pivMasterObj,q=1,t=1)
# print tMaster,rMaster
# print value
# if value == 1 :
#     cmds.setAttr (con ,0);


# cmds.select(cl=1)
# jnt = cmds.joint(n = 'BboxFix')
# cmds.parent(jnt,'root')
# cmds.setAttr((jnt+'.jointOrientX'),0)
# cmds.setAttr((jnt+'.jointOrientY'),0)
# cmds.setAttr((jnt+'.jointOrientZ'),0)
# cmds.setAttr((jnt+'.translateY'),-35)
# mel.eval('source cryExport.mel')
# mel.eval('cryExportWin')
# child =  cmds.listRelatives('CHR_g',c=1)
# cmds.parent(child[0],w=1)



####Remove  attributes

# sel =  cmds.ls(sl =1,type = 'joint')
# for i in range(0,len(sel)):
#     cmds.select(sel[i])
#     #cmds.setAttr((sel[i]+'.jointOrient'),l=0)
#     udAttr =  cmds.listAttr(r=1,ud=1)
#     try:
#         udAttr.remove('rotLimitMin0')
#         udAttr.remove('rotLimitMin1')
#         udAttr.remove('rotLimitMin2')
#         udAttr.remove('rotLimitMax0')
#         udAttr.remove('rotLimitMax1')
#         udAttr.remove('rotLimitMax2')
#         udAttr.remove('spring0')
#         udAttr.remove('spring1')
#         udAttr.remove('spring2')
#         udAttr.remove('springTension0')
#         udAttr.remove('springTension1')
#         udAttr.remove('springTension2')
#         udAttr.remove('damping0')
#         udAttr.remove('damping1')
#         udAttr.remove('damping2')
#     except:
#         print 'array is clean'
#     
#     try:
#                  
#         for j in range(0,len(udAttr)):        
#             cmds.deleteAttr(sel[i]+'.'+udAttr[j])
#             print 'Deleted attribite %s' , udAttr[j]
#     except:
#         print 'what a big deal'


# sel =  cmds.ls(sl=1)
# suffix =  '_Phys'
# prifix = '|group1'
# for i in range(0,len(sel)):
#     #cmds.select(sel[0])
#     parent =  sel[i].strip(suffix)
#     parent  =  parent.strip(prifix)
#     cmds.parent(sel[i],parent)
#     print parent, sel[i]


## to DO .. 
##make sure my self is loaded instead of red9
#mel cooomand toggleShelfTabs; and shelfTabChange; hint

# setAttr "joint_Leg_A_1_LT.rotXLimited" 1;
# setAttr "joint_Leg_A_1_LT.rotYLimited" 1;
# setAttr "joint_Leg_A_1_LT.rotZLimited" 1;
# setAttr "joint_Leg_A_1_LT.rotLimitMinX" -50;
# setAttr "joint_Leg_A_1_LT.rotLimitMinY" -50;
# setAttr "joint_Leg_A_1_LT.rotLimitMinZ" -50;
# setAttr "joint_Leg_A_1_LT.rotLimitMaxX" 50;
# setAttr "joint_Leg_A_1_LT.rotLimitMaxY" 50;
# setAttr "joint_Leg_A_1_LT.rotLimitMaxZ" 50;


# rotLim = ['.rotXLimited','.rotYLimited','.rotZLimited']
# rotLMin = ['.rotLimitMinX','.rotLimitMinY','.rotLimitMinZ']
# rotLMax = ['.rotLimitMaxX','.rotLimitMaxY','.rotLimitMaxZ']
# 
# sel =  cmds.ls(sl=1,type = 'joint')
# 
# for i in range(0,len(sel)):
#     for j in range(0,len(rotLim)):             
#         cmds.setAttr((sel[i]+rotLim[j]),1)
#         cmds.setAttr((sel[i]+rotLMin[j]),-50)
#         cmds.setAttr((sel[i]+rotLMax[j]),50)



#setAttr -type "string" joint_Pelvis|joint_Pelvis_Phys.UDP "mass=1";


# sel =  cmds.ls(sl=1,ap =1)
# for i in range(0,len(sel)):
#     cmds.setAttr((sel[i]+'.UDP'),'mass=1',type='string')


# import maya.cmds as cmds
# if cmds.commandPort(':7720', q=True) !=1:
#     cmds.commandPort(n=':7720', eo = False, nr = True)

    