# ------------------------------------------------------------------------------
# Patch Bake
# ------------------------------------------------------------------------------
# Bakes the selected patches to images manager
# Its the same as export current channel flattened 
# and load the image back to image manager
# (can be time saving)
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menue item in Patches > Patch Bake
# 
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari
import os

def patchBake():
	curGeo = mari.geo.current()
	patchList = list (curGeo.patchList() )
    selPatchList = [patch for patch in patchList if patch.isSelected() ]

	if len(selPatchList) == 0:
		mari.utils.meesage()
		return

   	mari.history.startMacro('Patch Bake')
    mari.app.setWaitCursor()

	user = os.popen('whoami').read().split()[0]
	path = str ('/home/'+ user + '/Desktop/tmp_bak_tmp.tga' )

	curChan = curGeo.currentChannel()
	layers = list (curChan.layerList())
	
	for layer in layers:
		layer.setSelected(True)
	
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	pasteAction = mari.actions.find('/Mari/Layers/Paste')
	pasteAction.trigger()
	
	curChan.mergeLayers()
	
	curLayer = curChan.currentLayer()
	curImgSet = curLayer.imageSet()
	
	for patch in selPatchList:
		uv = patch.uvIndex()
		
		patchImg = curImgSet.image(uv, -1)
		patchImg.saveAs(path)
	
		mari.images.load(path)
		os.remove(path)
	
	cur_chan.removeLayers()

	mari.app.restoreCursor()
	mari.history.stopMacro()

mari.menus.addAction(mari.actions.create('Patch Bake', 'patchBake()'), "MainWindow/Patches")