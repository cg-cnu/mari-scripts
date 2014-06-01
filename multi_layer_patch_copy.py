# ------------------------------------------------------------------------------
# Multi Layer-Patch Copy (WIP)
# ------------------------------------------------------------------------------
# Define Udim mapping 
# Specify the source patch from which paint data is copied from - to the target
# patch to wich data is copied.
#
# eg: source patch : target patch / source patch : target patch
#
# eg: 1:2 / 3 : 4 (read - Udim 1001 is copied to Udim 1002 and
#					Udim 1003 is copied to udim 1004) 
#
# eg: 1:4-8 / 10:15,21 (read - Udim 1001 copied to udim 1004,1005...1008 and
#						Udim 1010 is copied to Udim 1015 and 1021)
#
# The script works recursively and takes care of...
#	all the selected paintable layers.
#	all the layers inside the selected groups.
# 	all adjustment and other type of layers in the adjustment stacks.
# 	all the masks and mask staks on the all types of layers. 
#
# The udim mapping entered will be saved to a txt file in the log folder.
# You can recover it using 'recover Udim Mapping' button.
# 
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menu item in Patches > Multi Layer-Patch Copy
# 
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

## fix recover..

import mari
import os
import PythonQt

GUI = PythonQt.QtGui

def getPath():
	''' get the respective path '''
	
	if mari.app.version().isWindows():
		#user = os.popen('whoami').read().split('\\')[-1].rstrip("\n")
		#path = "C:/User/" + user + "/Documents/Mari/Logs/UDIMmappings.txt"
		pluginPath = str (mari.resources.path("MARI_USER_PATH")).replace("\\", "/")
		path = pluginPath + "/Logs/UDIMmappings.txt"
	else:
		user = os.popen('whoami').read().split()[0]
		path = str('/home/' + user + '/Mari/Logs/UDIMmappings.txt')
		
	return path

def getUdimMap(data):
	''' Updates the global variables sourcePatches and targetPatches
	from the udim mapping data user provides  '''	

	global sourcePatches, targetPatches

	sourcePatches = []
	targetPatches = []
	
	data = data.replace("\n", "")
	data = data.replace(' ', '')
	data2 = data.split('/')
	
	for i in data2:
		data3 = i.split(':')
		sourcePatches.append(int (data3[0]) - 1)

		tmp_values = []
		data4 = data3[1].split(",")

		for j in data4:

			if "-" not in j:
				tmp_values.append(int(j) - 1)
			else:
				k = j.split('-')
				l = range(int (k[0]), int(k[1]) + 1)

				for m in l:
					tmp_values.append(int(m) - 1)
		targetPatches.append(tmp_values)
	return

def getGroupLayers(group):
	''' Returns the list of layers for the given layer group '''

	groupStack = group.layerStack()
	layerList = groupStack.layerList()

	return layerList 

def copyPatches(imgSet):
	''' For the given imageset will copy the data
	from source patch to target patches '''

	for patch in sourcePatches:
		sourceImg = imgSet.image(patch, -1)
		
		index = sourcePatches.index(patch)
		target_patches = targetPatches[index]

		for each in target_patches:
			targetImg = imgSet.image(each, -1)
			targetImg.copyFrom(sourceImg)

	return

def getAllData():
	''' get all the necessary layer and patch data '''	
	global curGeo, curChan, allLayers
	global layers, grpLayers, selGroups, selLayers
	global patches, selPatches
	
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
			grpLayers += [ layer for layer in layers_in_grp if layer.isGroupLayer() ]

	layers = [layer for layer in allLayers if not layer.isGroupLayer() ]
	selLayers = [layer for layer in allLayers if layer.isSelected() ]		

	selGroups = [layer for layer in allLayers if layer.isGroupLayer() and layer.isSelected() ]		
	
	for group in selGroups:
		layers_in_grp = list (getGroupLayers(group))	

		for each in layers_in_grp:
			if each.isGroupLayer():
				selGroups.append(each)
			else:
				selLayers.append(each)

	return

def copyStacks(layers):
	''' copies the image sets'''	

	for layer in layers:
		if layer.isPaintableLayer():
			imgSet = layer.imageSet()
			copyPatches(imgSet)

		if layer.hasMask() and not layer.hasMaskStack():
			imgSet = layer.maskImageSet()
			copyPatches(imgSet)			

		try:
			if layer.hasMaskStack():
				mask_stack = layer.maskStack()
				mask_stack_elements = list (mask_stack.layerList())
				for layer in mask_stack_elements:
					layers.append(layer)
		except AttributeError:
			pass

		try:
			if layer.hasAdjustmentStack():
				adjust_stack = layer.adjustmentStack()
				adjust_stack_elements = adjust_stack.layerList()
				for layer in mask_stack_elements:
					layers.append(layer)
		except AttributeError:
			pass					

	return

def updateUdimMap(data):
	''' update the udim mapping to the file in logs '''

	path = getPath()
	objectName = str(curGeo.name())
	
	try:
		f = open(path, 'r')
		oldMappings = f.readline()
		f.close()
		index = None		

		for line in oldMappings:
			if line.startswith (objectName):
				index = oldMappings.index(line)

		if index != None:
			UdimMapFile = open(path, 'w')
			oldMappings[index + 1] = str (data) + '\n'

			for i in oldMappings:
				udimMapFile.write(str(i))

		else:
			udimMapFile = open(path, 'a')
			udimMapFile.write('\n' + objectName + '\n' + data)

	except IOError:
		udimMapFile = open(path, 'w')
		udimMapFile.write('\n' + objectName + '\n' + data)		

	return

def recoverUdimMap():
	''' recovers the udim mapping if any '''
	
	path = getPath()
	curGeo = mari.geo.current()
	objectName = str(curGeo.name())

	index = None

	try:
		with open(path, 'r') as f:
			oldMappings = f.readline()

		for line in oldMappings:
			if line.startswith(objectName):
				index = oldMappings.index(line)
				oldUDIMmap = oldMappings[index+1]
				field.setPlainText(oldUDIMmap)

		if index == None:
			mari.utils.message('no previous mappings')

	except IOError:
		mari.utils.message('no previous mappings')

	return

def multiLayerPatchCopy():
	''' copies the imgsets for the patches in the udim mapping '''

	data = field.toPlainText()
	if data == "":
		mari.utils.message('Please enter atleast one mapping in format source: targe')
		return

	getUdimMap(data)
	getAllData()
	updateUdimMap(data)

	mari.history.startMacro("Multi Layer-Patch Copy")

	if channelCheck.isChecked():
		copyStacks(allLayers)
	else:
		copyStacks(selLayers)

	mari.history.stopMacro()	
	
	layerPatchDialog.close()	

	return

#--------------------------- ui ----------------------------
layerPatchDialog = GUI.QDialog()
layerPatchDialog.setWindowTitle("Multi Layer-Patch Copy")

vLayout = GUI.QVBoxLayout()

layerPatchDialog.setLayout(vLayout)
layerPatchDialog.setGeometry(800,200,400,280)

recoverUdimMapButton = GUI.QPushButton ('Recover UDIM Mapping')
recoverUdimMapButton.connect ('clicked()', lambda: recoverUdimMap())
recoverUdimMapButton.setToolTip('Recover the previous udim mapping')
vLayout.addWidget(recoverUdimMapButton)

vLayout.addWidget(GUI.QLabel('UDIM Mapping'))

field = GUI.QTextEdit()
vLayout.addWidget(field)

channelCheck = GUI.QCheckBox('all Layers')
vLayout.addWidget(channelCheck)
channelCheck.setToolTip('copy for all the layers in the current channel')

copyButton = GUI.QPushButton('Copy')
copyButton.connect('clicked()', lambda: multiLayerPatchCopy())
copyButton.setToolTip('copy the patches in the udim map')
vLayout.addWidget(copyButton)

### show the ui
def showLayerPatchUi():
	'''display the ui'''

    if mari.projects.current() is None:
    	mari.utils.message('no project currently open')
		return
	
	layerPatchDialog.show()
	return
	
mari.menus.addAction(mari.actions.create('Multi Layer-Patch copy', 'showLayerPatchUi()'), 'MainWindow/Patches')
