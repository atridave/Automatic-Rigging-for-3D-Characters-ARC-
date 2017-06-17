'''
Created on Sep 8, 2016

@author: adave
'''
import os,inspect
import maya.cmds as cmds
import CORE.rigTemplate as rigTemp


class FileFolderInfo:
      
    
    def getModuleInfo(self,file):
        self.fullFilePath  =  inspect.getfile(file)
        self.dir = os.path.dirname(self.fullFilePath)
        return self.fullFilePath,self.dir   
        
        


class fileOperation:
    def __init__(self):
        self.templatePath = rigTemp   
    
    def printFilename(self,file):
        self.file =  file
        print self.file
    
    def loadMayaFile(self,filePath):        
        cmds.file(filePath,i =1 , f=1)
        
    def loadTemplateFile(self,template):
        self.template  = template
        if self.template  == "twoChainJoint":
            pass
            
            

path =  os.getcwd()
str = path.rsplit('CORE')
print str
print(len(str))





