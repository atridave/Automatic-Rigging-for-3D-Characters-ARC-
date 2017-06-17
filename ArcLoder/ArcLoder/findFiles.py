import os
import glob
import logging
import maya.cmds as cmds
path = 'F:\starcitizen\CryEngine\Data\Animations_Source\Characters\Human\male_v7\weapons\stocked\locomotion\crouch'
os.chdir(path)
print os.getcwd()
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
maExt =  '.ma'
fbxExt = '.fbx'
sourcefiles =  glob.glob('*'+maExt)
destinationFile =  glob.glob('*'+fbxExt)


def giveFileName(fullName,ext):
    filename = fullName.split(ext)[0]
    return filename

def getAllFiles(files,ext):
    filesShort = []
    
    for i in range(0,len(files)):
        fileName =  giveFileName(files[i],ext)
        filesShort.append(fileName)
        
    return filesShort



maFiles =  getAllFiles(sourcefiles,maExt)
fbxFiles =  getAllFiles(destinationFile,fbxExt)



cc = []
dd = []
for i in range(0,len(maFiles)):
    for j in range(0,len(fbxFiles)):
        if fbxFiles[j] == maFiles[i]:
            cc.append(fbxFiles[j])
        else :
            if not fbxFiles[j] in dd:
                dd.append(fbxFiles[j])
            

   
# print 'MAyaFiles which has FBX::',
# for i in range (0,len(cc)):
#     print( cc[i])
#     
# #print 'onlyFbx FBX::',
# #for i in range (0,len(dd)):
# #    print( dd[i])
# 
# print dd


#file -loadReference "bhm_skeletonRed9_PUBRN" -type "mayaAscii" -options "v=0;" "F:/starcitizen/CryEngine/Data/Objects/Characters/Human/male_v7/export/bhm_skeletonRed9_PUB.ma";
neRefFile = 'F:/starcitizen/CryEngine/Data/Objects/Characters/Human/male_v7/export/bhm_skeletonRed9_PUB.ma'
val =  len(sourcefiles)
val =1
for i in range (0,val):
    print sourcefiles[i]
    cmds.file(sourcefiles[i],open = 1,f=1)
    references = cmds.ls(type='reference')
    cmds.file(neRefFile,loadReference = references[0],options='v=0;',f=1)
    cmds.file(save = 1, f = 1)
    
    
# for ma in sourcefiles:
#     print ma
#     cmds.file(ma,open = 1,f=1)
#     #cmds.file(loadReference = 'bhm_skeletonRed9_PUBRN',type = 'mayaAscii',options ='v=0',neRefFile)
    






   





