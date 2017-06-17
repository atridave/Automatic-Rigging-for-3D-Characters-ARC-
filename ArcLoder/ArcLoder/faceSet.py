import maya.cmds as cmds
import maya.OpenMaya as om
# if multiple shaders are assigned to different sets of faces,
# create FACESET_ int array attributes for them (FACESET is recognized by alembic import/procedural)
# python/MEL sucks at face selections, so using the API

shp = 'yourPolyshape'

selList = om.MSelectionList()
selList.add(shp)
path = om.MDagPath()
selList.getDagPath(0, path)

fnMesh = om.MFnMesh(path)
shaders = om.MObjectArray()
faces = om.MIntArray()
fnMesh.getConnectedShaders(0, shaders, faces)
if shaders.length() > 1:
    faceIDs = [[] for x in xrange(shaders.length())]
    for i in range(faces.length()):
        faceIDs[faces[i]].append(i)
    for i in range(shaders.length()):
        attr = 'FACESET_' + str(i)
        if not cmds.attributeQuery(attr, node=shp, ex=True):
            cmds.addAttr(shp, dt='Int32Array', ln=attr)
        attr = shp + "." + attr
        cmds.setAttr(attr, faceIDs[i], type='Int32Array')

