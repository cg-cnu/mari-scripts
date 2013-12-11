# ------------------------------------------------------------------------------
# Toggle layer visibility and lock
# ------------------------------------------------------------------------------
# ctrl + shift + V - Toggles the visibility of selected layers 
# alt + shift + V - Toggles the visibility of Unselected layers
# ctrl + shift + L - Toggles the lock status of selected layers
# alt + shift + L - Toggles the lock status of unselected layers
# 
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates menue items in Layers 
# The default shortcut can be changed from Edit > shortcuts
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari

def getLayersInGroup(group):
    ''' given a group will return all the layers in the group '''

    groupStack = group.layerStack()
    layerList = groupStack.layerList()
    
    return layerList

def layerData():
    ''' Updates the global Variables of all the layers, selected Layers,
    unselected layers and groups, selected groups and unselected groups '''

    global layers, selLayers, unSelLayers
    global groups, selGroups, unSelGroups

    if not mari.projects.current():
        mari.utils.message('No project currently open')
        return -1
    
    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()

    layerList = list (curChan.layerList())    
    
    layers = [ layer for layer in layerList if not layer.isGroupLayer() ]
    selLayers = [ layer for layer in layers if layer.isSelected() ]
    unSelLayers = [ layer for layer in layers if not layer.isSelected() ]
    
    groups = [ layer for layer in layerList if layer.isGroupLayer() ]
    selGroups = [ group for group in groups if group.isSelected() ]
    unSelGroups = [ group for group in groups if not group.isSelected() ]

    if len(unSelGroups) != 0:
        
        for unSelGroup in unSelGroups:
            layersInGroup = list (getLayersInGroup(unSelGroup))

            for layer in layersInGroup:
                if layer.isGroupLayer():
                    if layer.isSelected():
                        selGroups.append(layer)
                    else:
                        unSelGroups.append(layer)
                else:
                    if layer.isSelected():
                        selLayers.append(layer)
                    else:
                        unSelLayers.append(layer)
    return

def toggleSelVisibility():
    ''' Toggles the visibility of the selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Visibility')
        mari.app.setWaitCursor()

        for layer in selLayers:
            layer.setVisibility(not layer.isVisible())
        for group in selGroups:
            group.setVisibility(not group.isVisible())
        
        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleUnselVisibility():
    ''' Toggles the visibility of the un selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Visibility')
        mari.app.setWaitCursor()

        for layer in unSelLayers:
            layer.setVisibility(not layer.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleSelLock():
    ''' Toggles the lock status of the selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Lock')
        mari.app.setWaitCursor()

        for layer in selLayers:
            layer.setLocked(not layer.isLocked())
        for group in selGroups:
            group.setLocked(not group.isLocked())
        
        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleUnselLock():
    ''' Toggles the lock status of the Unselected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Lock')
        mari.app.setWaitCursor()

        for layer in unSelLayers:
            layer.setLocked(not layer.isLocked())

        for group in unSelGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return
    
toggleSelVisibilityAction = mari.actions.create('Toggle Selected Visibility', 'toggleSelVisibility()')
mari.menus.addAction(toggleSelVisibilityAction, 'MainWindow/Layers')
toggleSelVisibilityAction.setShortcut('Ctrl+Shift+V')

toggleUnselVisibilityAction = mari.actions.create('Toggle Unselected Visibility', 'toggleUnselVisibility()')
mari.menus.addAction(toggleUnselVisibilityAction, 'MainWindow/Layers')
toggleSelVisibilityAction.setShortcut('Alt+Shift+V')

toggleSelLockAction = mari.actions.create('Toggle Selected Lock', 'toggleSelLock()')
mari.menus.addAction(toggleSelLockAction, 'MainWindow/Layers')
toggleSelLockAction.setShortcut('Ctrl+Shift+L')

toggleUnselLockAction = mari.actions.create('Toggle Unselected Lock', 'toggleUnselLock()')
mari.menus.addAction(toggleUnselLockAction, 'MainWindow/Layers')
toggleSelLockAction.setShortcut('Alt+Shift+L')