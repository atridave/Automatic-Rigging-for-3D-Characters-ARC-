'''
Created on Jun 15, 2017

@author: Admin
'''


from PySide.QtCore import *
from PySide.QtGui import *
import sys
import maya._OpenMayaUI as oui
import shiboken
import maya.cmds as cmds




def getMayaWindow():
    pointer =  oui.MQtUtil_mainWindow()
    return shiboken.wrapInstance(long(pointer),QWidget)




parent  =  getMayaWindow()
winObjName =  'MayaUserWindow'
window  =  QMainWindow(parent)
window.setObjectName(winObjName)

if cmds.window('MayaUserWindow',exists = 1):
    cmds.deleteUI('MayaUserWindow')

font  =  QFont()
font.setPointSize(12)
font.setBold(1)


button  =  QPushButton('createBox')
button.setMinimumSize(200,40)
button.setMaximumSize(200,40)
button.setFont(font)




widget =  QWidget()
window.setCentralWidget(widget)
layOut  =  QVBoxLayout(widget)
layOut.addWidget(button)

window.show()






def createBox():
    cmds.polyCube()
    

    
