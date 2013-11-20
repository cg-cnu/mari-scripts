# patch Bake
#
# bakes the slected patches to image manager
# Works like Patches > Extract Selected
# does for all the layers in the channel
#
# 

import mari
import os

def bakePatch():
	curGeo
	patchList
	selPatchList
	
	if len(selPatchList) == 0:
		mari.utils.meesage()
		return
	wait cursor
	user = os.popen('whoami').read().split()[0]
	path = str ('/home/'+ user + '/Desktop/tmp_bak_tmp.tga' )

	curChan
	Layers = 
	
	for layer in layers:
		layer.setSelected(True)
		
	# put the whole code here...
	merge_duplicate()
	
	cur_layer = curChan.currentLayer()
	curImgSet = cur_layer.imageSet()
	
	for patch in selPatchList:
		uv = patch.uvIndex()
		
		patchImg = curImgSet.image(uv, -1)
		patchImg.saveAs(path)
	
		mari.images.load(path)
		os.remove(path)
		
	cur_chan.removeLayers()

mari.app.restoreCursor()
mari.history.stopMacro()
