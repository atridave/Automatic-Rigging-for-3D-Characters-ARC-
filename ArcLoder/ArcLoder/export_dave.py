    def _daveHeadCamHack(self):
        _fileName  =  cmds.file( q=True, sn=1)
        _fbxName =  _fileName.replace('.ma','.fbx')
        pm.mel.FBXRead(f=_fbxName)
        takes = pm.mel.FBXGetTakeCount()
        frames = pm.mel.FBXGetTakeLocalTimeSpan(1)
        startFrame = frames[0]
        endFrame = frames[1]
        cmds.playbackOptions(e=1,ast =startFrame ,aet= endFrame )
        print startFrame , '  ' , endFrame
        cmds.file(save=1,type = 'mayaAscii',f=1)
                
        
        targetCtr = 'male_v7:src:Head_LowPass_Ctr'        
        locoCtr = 'male_v7:Locomotion_Ctr'
        
        cmds.xform(targetCtr, t = (7,25,150) )
         
       
        parentCon = cmds.parentConstraint(locoCtr,targetCtr,mo=1)
        startFrame = cmds.playbackOptions(q=1,min =1)
        endFrame = cmds.playbackOptions(q=1,max =1)
        cmds.bakeResults(targetCtr, t=(startFrame,endFrame),at=['tx','ty','tz',"rx","ry","rz"], simulation=True )
        cmds.delete(parentCon)
        cmds.playbackOptions(e=1,min =startFrame , max =endFrame, ast =startFrame ,aet= endFrame )
        cmds.file(save=1,type = 'mayaAscii',f=1)
        print ('I am saving ::::::::::::::::'+  _fileName)