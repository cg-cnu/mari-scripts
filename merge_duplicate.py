# ------------------------------------------------------------------------------
# Merge Duplicate
# ------------------------------------------------------------------------------
# creates a merge duplicate of selected layers.	
# Same as Command+Shift+E / Ctrl+Shift+E in photoshop
# Will merge for selected patches other wise will merge all.
# Will rename the merged layer to the current active layer name + _mrgDup
# ** rename will work for mari 2.5 and after **
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
	''' Creates a merge duplicate of the current selected layers '''
	
	if not mari.projects.current():
		mari.utils.message('No project currently open')
		return
	
	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()
	curActiveLayerName = str(curChan.currentLayer().name())
	
	patches = list(curGeo.patchList())
	unSelPatches = [ patch for patch in patches if not patch.isSelected() ]
	
	mari.app.setWaitCursor()
	mari.history.startMacro('Merge Duplicate')

	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	pasteAction = mari.actions.find('/Mari/Layers/Paste')
	pasteAction.trigger()
	
	curChan.mergeLayers()
	
	curLayer = curChan.currentLayer()

	if len(patches) != len(unSelPatches):
		
		imgSet = curLayer.imageSet()
		
		for patch in unSelPatches:
			uv = patch.uvIndex()
			patchImg = imgSet.image(uv, -1)
			patchImg.fill(mari.Color(1,0,0,0))
			
	if mari.app.version().number() >= 20501300:
		
		curLayer.setName(curActiveLayerName + '_mrgDup')

	mari.history.stopMacro()
	mari.app.restoreCursor()

	return

mergeDuplicateAction = mari.actions.create ('Merge Duplicate', 'mergeDuplicateLayers()')
mari.menus.addAction(mergeDuplicateAction, 'MainWindow/Layers')
mergeDuplicateAction.setShortcut('Ctrl+Shift+E')