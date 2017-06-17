'''
Created on 5 Jul 2016

@author: adave
'''
import os
import glob
import maya.cmds as cmds
path = 'D:\starcitizen\CryEngine\Data\Animations_Source\Characters\Human\male_v7\weapons\stocked\locomotion\stand' 
refFile = 'D:\starcitizen\CryEngine\Data\Objects\Characters\Human\male_v7\export\\'

print (refFile+'\bhm_skeletonRed9_PUB.ma')

def replaceReference(folderPath,refFile,ext):
    os.chdir(folderPath)
    sourcefiles =  glob.glob('*'+ext)       
    for i in range(0,1):
        print sourcefiles[i]
        cmds.file(sourcefiles[i],open = 1,f=1)
        references = cmds.ls(type='reference')
        print  references
        cmds.file((refFile+'bhm_skeletonRed9_PUB.ma'),loadReference = references[0],options='v=0;',f=1)
        cmds.file(save = 1, f = 1)
    


replaceReference(path,refFile,'.ma')

#len(sourcefiles)

