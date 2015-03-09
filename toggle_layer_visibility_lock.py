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

# ------------------------------------------------------------------------------    
# The following are used to find selections no matter where in the Mari Interface:
# returnTru(),_getLayerList(),_findLayerSelection()
# 
# This is to support a) Layered Shader Stacks b) deeply nested stacks (maskstack,adjustment stacks),
# as well as cases where users are working in pinned or docked channels without it being the current channel

# ------------------------------------------------------------------------------

def _returnTrue(layer):
    """Returns True for any object passed to it."""
    return True
    
# ------------------------------------------------------------------------------
def _getLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(_getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(_getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(_getLayerList(layer.adjustmentStack().layerList(), criterionFn))
        
    return matching
# ------------------------------------------------------------------------------

def _findLayerSelection():
    """Searches for the current selection if mari.current.layer is not the same as layer.isSelected"""
    
    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    channels = curGeo.channelList()
    curLayer = mari.current.layer()
    layers = ()
    layerList = ()
    chn_layerList = ()
    layerSelect = False
     
    if curLayer.isSelected():

        layerSelect = True 
        # Stepping through all substacks of current channel so it works in maskstacks etc.
        layerList = curChannel.layerList()
        layers = _getLayerList(layerList,_returnTrue)
        chn_layerList = layers

    else:
    
        for channel in channels:
            
            layerList = channel.layerList()
            layers = _getLayerList(layerList,_returnTrue)
        
            for layer in layers:
    
                if layer.isSelected():
                    chn_layerList = layers
                    curChannel = channel
                    layerSelect = True

    
    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')


    return curChannel,chn_layerList

# ------------------------------------------------------------------------------


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
    
    geo_data_list = _findLayerSelection()
    layerList = list (geo_data_list[1])    
    
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
    



# ----------------------UI INTEGRATION-------------------------------#

###  Toggle Layer Visbility ###

UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
script_menu_path = 'MainWindow/Scripts/Layers/' + u'Visibility + Lock'


toggleSelVisibilityItem = mari.actions.create('Toggle Selected Visibility', 'toggleSelVisibility()')
mari.menus.addAction(toggleSelVisibilityItem, UI_path, 'Remove Layers')
mari.menus.addAction(toggleSelVisibilityItem, script_menu_path)

icon_filename = 'ToggleVisibility.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
toggleSelVisibilityItem.setIconPath(icon_path)
toggleSelVisibilityItem.setShortcut('Ctrl+Shift+V')

toggleUnselVisibilityItem = mari.actions.create('Toggle Unselected Visibility', 'toggleUnselVisibility()')
mari.menus.addAction(toggleUnselVisibilityItem, UI_path)
mari.menus.addAction(toggleUnselVisibilityItem, script_menu_path)

icon_filename = 'ToggleVisibility.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
toggleUnselVisibilityItem.setIconPath(icon_path)
toggleUnselVisibilityItem.setShortcut('Alt+Shift+V')


# --------------------------------------------------------------------

###  Toggle Layer Lock ###

UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
script_menu_path = 'MainWindow/Scripts/Layers/Visibility + Lock'

toggleSelLockItem = mari.actions.create('Toggle Selected Lock', 'toggleSelLock()')
mari.menus.addAction(toggleSelLockItem, UI_path)
mari.menus.addAction(toggleSelLockItem, script_menu_path)

icon_filename = 'Lock.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
toggleSelLockItem.setIconPath(icon_path)
toggleSelLockItem.setShortcut('Ctrl+Shift+L')

toggleUnselLockItem = mari.actions.create('Toggle Unselected Lock', 'toggleUnselLock()')
mari.menus.addAction(toggleUnselLockItem, UI_path)
mari.menus.addAction(toggleUnselLockItem, script_menu_path)

icon_filename = 'Lock.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
toggleUnselLockItem.setIconPath(icon_path)
toggleUnselLockItem.setShortcut('Alt+Shift+L')

# --------------------------------------------------------------------

###  Lock/Visibility Separator Main Interface ###

mari.menus.addSeparator(UI_path,'Toggle Selected Lock')
mari.menus.addSeparator('MainWindow/&Layers/','Remove Layers')


