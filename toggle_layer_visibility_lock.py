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

def findParentLayerStack(layer,layer_stack):
      "Returns the direct parent layer stack of the layer starting the search from the layer_stack"
      for search_layer in layer_stack.layerList():
          if search_layer==layer:
              return layer_stack
          if search_layer.isGroupLayer():
              result = findParentLayerStack(layer,search_layer.groupStack())
              if result is not None:
                  return result
          elif search_layer.hasMaskStack():
              result = findParentLayerStack(layer,search_layer.maskStack())
              if result is not None:
                  return result
      return None

# ------------------------------------------------------------------------------

def returnTrue(layer):
    """Returns True for any object passed to it."""
    return True

# ------------------------------------------------------------------------------
def getLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching_layer = []
    for layer in layer_list:
        if criterionFn(layer):
            matching_layer.append(layer)
        if hasattr(layer, 'layerStack'):
            matching_layer.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching_layer.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching_layer.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))

    return matching_layer
# ------------------------------------------------------------------------------

def findLayerSelection():
    """Searches for the current selection if mari.current.layer is not the same as layer.isSelected and returns a full list of layers of parent stacks"""

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    channels = curGeo.channelList()
    curLayer = mari.current.layer()

    layers = ()
    layerList = ()
    selectionList = []
    layerSelect = False
    parentLayers = []


    # If the current layer is selected I am assuming that the user has the channel selected as well
    if curLayer.isSelected():
        layerList = curChannel.layerList()
        layers = getLayerList(layerList,returnTrue)

        # scan layers in channels for selection and append to selectionList
        for layer in layers:
            if layer.isSelected():
                selectionList.append(layer)
                layerSelect = True

    # If the current layer is not selected go hunting for the selection in all channels
    else:
        for channel in channels:

            layerList = channel.layerList()
            layers = getLayerList(layerList,returnTrue)

            # scan layers in channels for selection and append to selectionList
            for layer in layers:
                if layer.isSelected():
                    selectionList.append(layer)
                    curChannel = channel
                    layerSelect = True


    # if nothing found:
    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')
        return


    # For each selected layer find the parent layerStack. For example for layers in groups this means the group
    for layer in selectionList:
        parents = findParentLayerStack(layer,curChannel)

        # for each parent LayerStack generate a full list of its layers and append one by one to parentLayers variable
        layer_list = parents.layerList()
        for layer in layer_list:
            parentLayers.append(layer)


    return parentLayers

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

    layerList = findLayerSelection()

    layers = [ layer for layer in layerList if not layer.isGroupLayer() ]
    selLayers = [ layer for layer in layers if layer.isSelected() ]
    unSelLayers = [ layer for layer in layers if not layer.isSelected() ]

    groups = [ layer for layer in layerList if layer.isGroupLayer() ]
    selGroups = [ group for group in groups if group.isSelected() ]
    unSelGroups = [ group for group in groups if not group.isSelected() ]


    return

def toggleSelVisibility():
    ''' Toggles the visibility of the selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Visibility')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()
        for layer in selLayers:
            layer.setVisibility(not layer.isVisible())
        for group in selGroups:
            group.setVisibility(not group.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleUnselVisibility():
    ''' Toggles the visibility of the un selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Visibility')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in unSelLayers:
            layer.setVisibility(not layer.isVisible())
        for group in unSelGroups:
            group.setVisibility(not group.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleSelLock():
    ''' Toggles the lock status of the selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Lock')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in selLayers:
            layer.setLocked(not layer.isLocked())
        for group in selGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleUnselLock():
    ''' Toggles the lock status of the Unselected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Lock')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in unSelLayers:
            layer.setLocked(not layer.isLocked())

        for group in unSelGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


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


