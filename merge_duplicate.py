# ------------------------------------------------------------------------------
# Merge Duplicate
# ------------------------------------------------------------------------------
# creates a merge duplicate of selected layers.	
# Same as Command+Shift+E / Ctrl+Shift+E in photoshop
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
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
