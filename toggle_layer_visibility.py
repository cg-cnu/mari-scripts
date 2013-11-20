def visibility():

	curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()
    patches = list (curGeo.patchList() )
    selPatches = [patch for patch in patches if patch.isSelected() ]
    allLayers = list (curChan.layerList())
    
    grpLayers = [layer for layer in allLayers if layer.isGroupLayer()]

    if len(grpLayers) != 0:
    	for group in grpLayers:
    		layers_in_grp = list (getGroupLayers(group))
            for each in layers_in_grp:
            	allLayers.append(each)
                    
			grpLayers += [ layer for layer in layers_in_grp if layer.isGroupLayer() == True]        
                    
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
	
toggleVisibilityAction = mari.asctions.create('Toggle Visibility', 'visibility()')
mari.menus.addAction(toggleVisibilityAction, 'MainWindw/Layers')
toggleVisibilityAction.setShortcut('Ctrl+Shift+V')
