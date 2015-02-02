# ------------------------------------------------------------------------------
# Patch Bake
# ------------------------------------------------------------------------------
# Bakes the selected patches to images manager.
# Works the same as patches > extract selected but for the whole channel
# and on all the selected patches.
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menu item in Patches > Patch Bake
# 
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari
import os

def patchBake():
	'''Bake the selected patches to image manager'''
	
	if not mari.projects.current():
		mari.utils.message('No project currently open', title = 'Error')
		return

	curGeo = mari.geo.current()
	patchList = list (curGeo.patchList() )
	selPatchList = [patch for patch in patchList if patch.isSelected() ]
	
	if len(selPatchList) == 0:
		mari.utils.meesage('Select atleast one patch', title = 'Error')
		return
	
	if mari.app.version().isWindows():
		path = str(mari.resources.path("MARI_USER_PATH")).replace("\\", "/")
	else:
		path = str( mari.resources.path("MARI_USER_PATH") )	

	curChan = curGeo.currentChannel()
	curChanName = str(curChan.name())
	
	layers = curChan.layerList()
	
	mari.history.startMacro('Patch Bake to Image Manager')
	mari.app.setWaitCursor()
	
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
		try: 
		
			uv = patch.uvIndex()
			
			curPatchIndex = str(patch.udim())
			savePath = path + curChanName + '.' + curPatchIndex + '.tif'
			
			patchImg = curImgSet.image(uv, -1)
			patchImg.saveAs(savePath)
		
			mari.images.load(savePath)
			os.remove(savePath)

		except Exception:
			
			pass
	
	
	curLayer.setName('BakeToImageManager')
	curChan.removeLayers()
	
	mari.history.stopMacro()
	mari.app.restoreCursor()



###   Patch Bake to Image Manager UI Integration

UI_path = 'MainWindow/&Patches'
script_menu_path = 'MainWindow/Scripts/Patches'

PatchToImageMgr= mari.actions.create('Patch to Image Manager', 'patchBake()')
mari.menus.addAction(PatchToImageMgr, UI_path,'UV Mask to Image Manager')
mari.menus.addAction(PatchToImageMgr, script_menu_path)

icon_filename = 'SaveToImageManager.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
PatchToImageMgr.setIconPath(icon_path)
PatchToImageMgr.setShortcut('')


# --------------------------------------------------------------------


###  Menu Separator ###

mari.menus.addSeparator(UI_path,'UV Mask to Image Manager')