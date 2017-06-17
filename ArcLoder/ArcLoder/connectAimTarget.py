import maya.cmds as cmds

def connectAimTarget(aimZeroG=None):
    pubNameSpace = 'bhm_skeletonRed9_PUB:'
    srcNameSpace = 'bhm_skeletonRed9_SRC:'
    hookSlot = ['RightWeaponBone','LeftWeaponBone','RightWeaponBone','LeftHand','RightHand']
    hooks = ['RightWeapon_Ctr','LeftWeapon_Ctr','CustomAim_Ctr','LHand2Aim_IKTarget_Ctr','RHand2Aim_IKTarget_Ctr']
    
    for i in range(len(hooks)):
        
        if i < 2 :
            hookSlotNameSpace  = ''
        else :
            hookSlotNameSpace = pubNameSpace+srcNameSpace
            
        cmds.pointConstraint((hookSlotNameSpace+hookSlot[i]),(pubNameSpace+hooks[i]))
        cmds.orientConstraint((hookSlotNameSpace+hookSlot[i]),(pubNameSpace+hooks[i]))
        if i > 2:
            cmds.setAttr(pubNameSpace+hooks[i]+'.blend',100)        
        print( (hookSlotNameSpace+hookSlot[i]) +'----->' + (pubNameSpace+hooks[i]))
          
    if aimZeroG ==1:
        cmds.orientConstraint((pubNameSpace+'Main_Ctr'),(pubNameSpace+'AimZeroG_Ctr'))

#connectAimTarget()
