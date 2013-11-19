# ------------------------------------------------------------------------------
# Multi Layer-Patch Copy
# ------------------------------------------------------------------------------
#
#  
# 
# Written by sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------
import mari
import os
import PythonQt


GUI = PythonQt.QtGui

def getUdimMap(data):
	''' get the udim mapping from the given data '''	
	global sourcePatches, targetPatches
	
	sourcePatches = []
	targetPatches = []
	
	data0 = data.replace("\n", "")
	data1 = data0.replace(' ', '')
	data2 = data1.split('/')
	
	for i in data2:
		data3 = i.split(':')
		sourcePatches.append(int (data3[0]) - 1)
		if "," in data3[1]:
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
		else:
			data4 = data3[1]
			tmp_values = []
			if '-' not in data4:
				tmp_values.append(int(data4)  - 1)
			else:
				k = data4.split('-')
				l = range(int(k[0]), int(k[1]) + 1)
				for m in l:
					tmp_values.append(int(m) - 1)
			targetPatches.append(tmp_values)

	return

def getGroupLayers(group):
	''' get the layrs in the group for the given group layer '''
	groupStack = group.layerStack()
	layerList = groupStack.layerList()
	return layerList 


def copyPatches(imgSet):
	''' copies the patches for the given image sets '''	
	for patch in sourcePatches:
		sourceImage = imgSet.image(patch, -1)
		
		ind = sourcePatches.index(patch)
		target_patches = targetPatches[index]
		for each in target_patches:
			targetImg = imgSet.image(each, -1)
			targetImg = copyFrom(sourceImg)

	return


def getAllData():
	''' get all the necessary data '''	
	global all
	
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
	user = os.popen('whoami').read().split()[0]
	path = '/home/' + user + '/Mari/Logs/UDIMmappings.txt'
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
		udimMapFile = open(path, 'W')
		udimMapFile.write('\n' + objectName + '\n' + data)
		
	return

def recoverUdimMap():
	''' recovers the udim mapping if any '''
	user = os.popen('whoami').read().split()[0]
	path = '/home/' + user + '/Mari/Logs/UDIMmappings.txt'
	curGeo = mari.geo.current()
	objectName = str(curGeo.name())
	index = None
	
	try:
		with open(path, 'r') as f:
			oldMappings = f.readline()
		for line in oldMappings:
			if line.startswith(object):
				index = oldMappings.index(line)
				oldUDIMmap = oldMappings[index+1]
				field.setPlainText(oldUDIMmap)

		if index == None:
			mari.utils.message('no prev mappings')

	except IOError:
		mari.utils.message('no previous mappings')
	return

def multiLayerPatchCopy():
	''' copies the imgsets for the patches in the udim mapping '''	
	data = field.toPlainText()
	if data == "":
		mari.utils.message('erere')
		return
	getUdimMap(data)
	getAllData()
	updateUdimMap(data)
	mari.history.startMacro("Multi Layer-Patch Copy")

	if channerlCheck.isChecked():
		copyStacks(allLayers)
	else:
		copyStacks(selLayers)

	mari.history.stopMacro()
	
	return

#--------------------------- ui ----------------------------
layerPatchdialog = GUI.QDialog()
layerPatchdialog.setWindowTitle("Multi Layer-Patch Copy")

vLayout = GUI.QVBoxLayout()

layerPatchdialog.setLayout(vLayout)
layerPatchdialog.setGeometry(800,200,400,280)

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
	
mari.menus.addAction(mari.actions.create('Multi Layer-Patch copy', 'showLayerPatchUi()'), 'MainWindow/Patches')