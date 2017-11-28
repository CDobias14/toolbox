### Nodal Parent Constraint function.
# Function creates a node based parent constraint using matrices.
# As with a standard parent constraint, select the driver first and the driven second.
# Unlike a standard parent constraint, you cannot constrain an object to multiple drivers. The driven object can only accept a single driver.
# Function automatically calculates and includes offset.
# WARNING: Function does not behave well when driving joints! Joints may serve as drivers, but may break if driven.
###

def nodalParentConstraint(*args):
    # Get the selected nodes
    sel = cmds.ls(sl = True)
    
    # Check that exactly two nodes are selected
    if len(sel) != 2:
        print("Must select exactly two nodes")
        return
    
    # Create multMatrix and decomposeMatrix nodes
    cmds.shadingNode('decomposeMatrix', asUtility = True, n = '{}_mtx2srt'.format(sel[1]))
    cmds.shadingNode('multMatrix', asUtility = True, n = '{}_mtxOffset'.format(sel[1]))
    
    # Connect nodes for offset
    cmds.connectAttr('{}.wm[0]'.format(sel[0]), '{}_mtxOffset.i[1]'.format(sel[1]), f = True)
    cmds.connectAttr('{}.wim[0]'.format(sel[1]), '{}_mtxOffset.i[2]'.format(sel[1]), f = True)
    cmds.connectAttr('{}_mtxOffset.o'.format(sel[1]), '{}_mtx2srt.imat'.format(sel[1]), f = True)
    
    # Get and set offset
    cmds.shadingNode('multMatrix', asUtility = True, n = '{}_tempForOffset'.format(sel[1]))
    cmds.connectAttr('{}.wm[0]'.format(sel[1]), '{}_tempForOffset.i[0]'.format(sel[1]), f = True)
    cmds.connectAttr('{}.wim[0]'.format(sel[0]), '{}_tempForOffset.i[1]'.format(sel[1]), f = True)
    offset = cmds.getAttr('{}_tempForOffset.o'.format(sel[1]))
    cmds.setAttr('{}_mtxOffset.i[0]'.format(sel[1]), offset, type = 'matrix')
    cmds.delete('{}_tempForOffset'.format(sel[1]))
    
    # Clean up connections
    cmds.connectAttr('{}.pim[0]'.format(sel[1]), '{}_mtxOffset.i[2]'.format(sel[1]), f = True)
    cmds.connectAttr('{}_mtx2srt.ot'.format(sel[1]), '{}.t'.format(sel[1]), f = True)
    cmds.connectAttr('{}_mtx2srt.or'.format(sel[1]), '{}.r'.format(sel[1]), f = True)
    cmds.connectAttr('{}_mtx2srt.os'.format(sel[1]), '{}.s'.format(sel[1]), f = True)
