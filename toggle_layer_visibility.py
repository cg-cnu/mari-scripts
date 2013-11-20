# ------------------------------------------------------------------------------
# Toggle layer visibility
# ------------------------------------------------------------------------------
# Toggles the visibility of selected layers
# Can be handy to turn of slected layers and compare the difference
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menue item in Layers > Toggle Layer Visibility
# The default shortcut has been kept to ctrl+shift+V
# Which can be changed from Edit > shortcuts
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

def visibility():

	curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()

    allLayers = list (curChan.layerList())    
    grpLayers = [layer for layer in allLayers if layer.isGroupLayer()]

    if len(grpLayers) != 0:
    	for group in grpLayers:
    		layers_in_grp = list (getGroupLayers(group))
            for each in layers_in_grp:
            	allLayers.append(each)
                    
			grpLayers += [ layer for layer in layers_in_grp if layer.isGroupLayer() ]        
                    
    layers = [layer for layer in allLayers if not layer.isGroupLayer() ]                
    selGroups = [layer for layer in allLayers if layer.isGroupLayer() and layer.isSelected() ]                
    selLayers = [layer for layer in allLayers if not layer.isSelected() ]                

    for group in selGroups:
		layers_in_grp = list (getGroupLayers(group))
    
        for each in layers_in_grp:
        	if each.isGroupLayer():
            	selGroups.append(each)
			else:
            	selLayers.append(each)
	
	mari.history.startMacro('Toggle Layer Visibility')
	for layer in sel_layers:
		layer.setVisibility(not layer.isVisible())
	for group in sel_groups:
		group.setVisibility(not layer.isVisible())
	mari.history.stopMacro()
	
	return
	
toggleVisibilityAction = mari.asctions.create('Toggle Layer Visibility', 'visibility()')
mari.menus.addAction(toggleVisibilityAction, 'MainWindw/Layers')
toggleVisibilityAction.setShortcut('Ctrl+Shift+V')