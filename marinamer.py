# ------------------------------------------------------------------------------
# marinamer
# ------------------------------------------------------------------------------
# rename multiple layers and assign colors.
#
# select a bunch of layers and assign  
#	prefix - sepeprator - layer name - seperator - suffix - num/abc - color
#
# > The existing layer name will be used if 'layer name' is empty	
# > You can rename even the layers/adjustment layers in 
#   the groups / adjustment stacks / mask stacks.
# > Autofill terms can be edited at /logs/texTerms.txt 
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menu item in Tools > marinamer
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari
import PySide
import string

GUI = PySide.QtGui

class Dialog(GUI.QDialog):

	def __init__(self):
		super(Dialog, self).__init__()

		self.alphabets = list( string.ascii_lowercase )
		self.seperators = ["N", " ","_", "-", "/", "+", ".", ","]
		self.sequenceList = ["NAN", "001", "abc"]
		self.colors = ["color", "black", "cyan", "dark blue",
						"light blue", "light green", "red",
						 "white", "yellow"] 

		self.setWindowTitle("marinamer")
		self.setGeometry(680, 400, 800, 60)

		mainLayout = GUI.QVBoxLayout()
		self.setLayout(mainLayout)

		renameLayout = GUI.QHBoxLayout()
		mainLayout.addLayout(renameLayout)

		self.prefix = GUI.QLineEdit()
		self.prefix.setPlaceholderText("prefix")

		renameLayout.addWidget(self.prefix)

		self.prefixSeperator = GUI.QComboBox()
		renameLayout.addWidget(self.prefixSeperator)
		self.prefixSeperator.addItems(self.seperators)

		self.layerName = GUI.QLineEdit()
		self.layerName.setPlaceholderText("layer name")
		renameLayout.addWidget(self.layerName)

		self.suffixSeperator = GUI.QComboBox()
		renameLayout.addWidget(self.suffixSeperator)
		self.suffixSeperator.addItems(self.seperators)

		self.suffix = GUI.QLineEdit()
		self.suffix.setPlaceholderText("suffix")
		renameLayout.addWidget(self.suffix)

		self.numberSeperator = GUI.QComboBox()
		renameLayout.addWidget(self.numberSeperator)
		self.numberSeperator.addItems(self.seperators)

		self.layerNumber = GUI.QComboBox()
		renameLayout.addWidget(self.layerNumber)
		self.layerNumber.addItems(self.sequenceList)

		self.layerColor = GUI.QComboBox()
		renameLayout.addWidget(self.layerColor)
		self.layerColor.addItems(self.colors)

		optionsLayout = GUI.QHBoxLayout()
		mainLayout.addLayout(optionsLayout)

		self.renameBtn = GUI.QPushButton("rename")
		self.renameBtn.clicked.connect(lambda: self.rename())
		optionsLayout.addWidget(self.renameBtn)

		self.renameBtn = GUI.QPushButton("reset")
		self.renameBtn.clicked.connect(lambda: self.resetUi())
		optionsLayout.addWidget(self.renameBtn)

		self.closeBtn = GUI.QPushButton("close")
		self.closeBtn.clicked.connect(lambda: self.cancel())
		optionsLayout.addWidget(self.closeBtn)
		
		self.texTerms = []
		self.loadtexTerms()
		self.setTexTermQCompleter()


	def resetUi(self):
		''' reset the ui for the data '''

		self.prefix.clear()
		self.layerName.clear()
		self.suffix.clear()

		self.prefixSeperator.setCurrentIndex(0)
		self.suffixSeperator.setCurrentIndex(0)
		self.numberSeperator.setCurrentIndex(0)
		self.layerNumber.setCurrentIndex(0)
		self.layerColor.setCurrentIndex(0)

	def getLayersInGroup(self, group):
		''' given a group returns all the layers in the group '''
	
		tmpLayersInGroup = list( group.groupStack().layerList() )

		for layer in tmpLayersInGroup:
			self.layerList.append(layer)

			if layer.isGroupLayer():
				self.getLayersInGroup(layer)


	def getLayersInAdjStack(self, layer):
		''' given a layer returns all the alyers inside the adjustment stack '''

		layersInAdjStack = []
		try:
			if layer.hasAdjustmentStack():
				layersInAdjStack = list ( layer.adjustmentStack().layerList() )

				for layer in layersInAdjStack:
					self.layerList.append(layer)

					if layer.isGroupLayer():
						self.getLayersInGroup(layer)

		except:
			pass


	def getLayersInMaskStack(self, layer):
		''' given a layer returns maskStack '''

		layersInMaskStack = []
		try:
			if layer.hasMaskStack():
				layersInMaskStack = list ( layer.maskStack().layerList() )

				for layer in layersInMaskStack:
					self.layerList.append(layer)

					if layer.isGroupLayer():
						self.getLayersInGroup(layer)
		except:
			pass


	def getSelLayers(self):
		''' given a layer returns all the layers including the masks and mask stacks '''

		curGeo = mari.geo.current()
		curChan = curGeo.currentChannel()

		self.layerList = list (curChan.layerList())
		groups = [ layer for layer in self.layerList if layer.isGroupLayer() ]

		for group in groups:
			self.getLayersInGroup(group)
			self.getLayersInAdjStack(group)
			self.getLayersInMaskStack(group)

		for layer in self.layerList:
			self.getLayersInAdjStack(layer)
			self.getLayersInMaskStack(layer)

		self.selLayers = [layer for layer in self.layerList if layer.isSelected() ]


	def appendTexTerms(self, term):
		''' update the texTerms list '''
		
		if term not in self.texTerms:
			self.texTerms.append(term)


	def setTexTermQCompleter(self):
		''' set the completer to the ui '''

		self.texCompleter = GUI.QCompleter(self.texTerms, self)
		self.texCompleter.setCompletionMode(GUI.QCompleter.PopupCompletion)

		self.prefix.setCompleter(self.texCompleter)
		self.suffix.setCompleter(self.texCompleter)
		self.layerName.setCompleter(self.texCompleter)


	def getSeperators(self, index):
		''' get the seperators '''

		if index == 0:
			seperatorText = ""
		else:
			seperatorText = self.seperators[ index ]

		return seperatorText


	def getNewLayerName(self, index, layer):
		''' get the final name to be renamed'''

		prefixText = self.prefix.text()
		self.appendTexTerms(prefixText)

		prefixSeperatorText = self.getSeperators( self.prefixSeperator.currentIndex() )

		layerNameText = self.layerName.text()

		self.appendTexTerms(layerNameText)
		if layerNameText == "":
			layerNameText = layer.name()

		suffixSeperatorText = self.getSeperators( self.suffixSeperator.currentIndex() )

		suffixText = self.suffix.text()
		self.appendTexTerms(suffixText)
		
		numberSeperatorText = self.getSeperators( self.numberSeperator.currentIndex() )
		
		if self.layerNumber.currentIndex() == 1:
			sequence =  str(index + 1 )

		elif self.layerNumber.currentIndex() == 2:
			sequence = self.alphabets[index]

		else:
			sequence = ""

		newName = prefixText + prefixSeperatorText + layerNameText + suffixSeperatorText 
		newName	= newName + suffixText + numberSeperatorText + sequence

		self.setTexTermQCompleter()

		return newName


	def getColor(self):
		''' get the color from the ui '''

		colorIndex = self.layerColor.currentIndex()

		if colorIndex == 0:
			color = "none"
		else:
			color = self.colors[colorIndex]

		return color


	def rename(self):
		''' main func to rename '''

		self.getSelLayers()

		selectedLayers = self.selLayers
		mari.history.startMacro("marinamer")

		for index, layer in enumerate(selectedLayers):

			newName = self.getNewLayerName(index, layer)
			layer.setName(newName)

			color = self.getColor()
			layer.setColorTag(color)
			
		mari.history.stopMacro()
		self.updateTexTerms()


	def loadtexTerms(self):
		''' load the list from the temp file '''

		try:
			file = open('texTerms.txt', 'r')
			self.texTermsList = file.readlines()
			self.texTerms = [ term.rstrip("\n") for term in self.texTermsList ]
		except IOError:
			# text terms file dosen't exist-ignore
			pass


	def updateTexTerms(self):
		''' update the list in a temp file '''

		with open('texTerms.txt', 'w') as myFile:
			for term in self.texTerms:
				myFile.write(term + "\n")


	def cancel(self):
		''' shutdown the ui '''

		self.close()


	def showUi(self):
		''' display ui ''' 

		if not mari.projects.current(): 
			mari.utils.message("No project currently open")
			return

		self.show()


MAIN = Dialog()
mari.menus.addAction(mari.actions.create('marinamer', 'MAIN.showUi()'), "MainWindow/Tools")
