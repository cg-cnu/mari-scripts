# ------------------------------------------------------------------------------
# Merge Duplicate
# ------------------------------------------------------------------------------
# 
# Merge a copy of all selected layers into a new layer	
# Command+Shift+E / Ctrl+Shift+E in photoshop
#
# Creates a menue item in Layers > Merge Duplicate 
# The default shortcut has been kept to ctrl+shift+E
# Which can be changed from Edit > shortcuts
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari

def mergeDuplicateLayers():
	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()
	curLayerName = str (curChan.currentLayer().name())
	
	mari.history.startMacro('Merge Duplicate')
	mari.app.setWaitCursor()
	
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	pasteAction = mari.actions.find('/Mari/Layers/Paste')
	pasteAction.trigger()
	
	curChan.mergeLayers()
		
	mari.history.stopMacro()
	mari.app.restoreCursor()	
	
mergeDuplicateAction = mari.actions.create ('Merge Duplicate'. 'mergeDuplicateLayers()')
mari.menus.addAction(mergeDuplicateAction, 'MainWindow/Layers')
mergeDuplicateAction.setShortcut('Ctrl+Shift+E')
