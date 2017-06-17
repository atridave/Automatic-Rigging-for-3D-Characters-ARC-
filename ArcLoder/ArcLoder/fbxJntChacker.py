'''
Created on 18 Mar 2016

@author: adave
'''


import maya.cmds as cmds
import DailyTool as dt
reload(dt)

def fbxJntChacker(mobuRootJnt,nameSpace):
    mobuJoints = [] 
    mobuAll = dt.DailyTool().sHI(mobuRootJnt)
    for i in range(0,len(mobuAll)):
        if cmds.nodeType(mobuAll[i]) == 'joint':
            mobuJoints.append(mobuAll[i])
            SRCJnt =  (nameSpace+(mobuAll[i]))
            loopJnt = [(mobuAll[i]),(nameSpace+(mobuAll[i]))]
            mobuXFormJnt = dt.getXform(mobuAll[i],1,1)
            SRCXFormJnt = dt.getXform(SRCJnt,1,1)
            cmds.select(SRCJnt)
            
            print (mobuAll[i])
            print mobuXFormJnt.Xval
            print SRCXFormJnt.Xval
            
#             for j in range(0,len(loopJnt)):
#                 XFormJnt = dt.getXform(loopJnt[j],1,1)
#                 print(loopJnt[j]),(XFormJnt.Xval) 

#             for j in range(0,len(mobuXFormJnt.Xval)):
#                 trans = ['postion','rotation']
#                 print (mobuAll[i]+('  joint'+trans[j])), ('------->'), ( mobuXFormJnt.Xval[j])        
#     
#     
    

    

   

    
    

    

    



fbxJntChacker('World','bhm_skeletonRed9_PUB:src:')


