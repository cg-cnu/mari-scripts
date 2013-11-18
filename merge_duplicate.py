# ------------------------------------------------------------------------------
# Merge Duplicate
# ------------------------------------------------------------------------------
# 
# Merge a copy of all selected layers into a new layer	
# Command+Shift+E / Ctrl+Shift+E in photoshop
# 
# Written by sreenivas alapati
# ------------------------------------------------------------------------------

import mari

def mergeDuplicateLayers():
	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()
	curLayerName = str (curChan.currentLayer().name())
	
	mari.history.startMacro('Merge Duplicate')
	
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	curChan.mergeLayers()
	
	if str (mari.app.version().string()) = '2.5v1':
		curLayer = curChan.currentLayer()
		curLayer.setName(curLayerName + '_mrgDup')
	
	mari.history.stopMacro()
	
mergeDuplicateAction = mari.actions.create ('Merge Duplicate'. 'mergeDuplicateLayers()')
mari.menus.addAction(mergeDuplicateAction, 'MainWindow/Layers')
mergeDuplicateAction.setShortcut('Ctrl+Shift+E')
