# ------------------------------------------------------------------------------
# Export Images from image manager
# ------------------------------------------------------------------------------
# export selected images from the image manager
# ** Mari >= 2.6 compatible **
#
# If the image has .format, it exports in the same format.
# otherwise it exports in .tga format.
# overwrites the file if it already exits.
#
# copy the script to the same location as your log folder in
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menue item in Tools > Export Images
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari
from PythonQt import QtGui, QtCore
import os

class ProgressDialog(QtGui.QDialog):

	def __init__(self, maxStep):
		super(ProgressDialog, self).__init__()
		self.setWindowTitle('Exporting Images...')

		self.cancelCpy = False

		layout = QtGui.QVBoxLayout()
		self.setLayout(layout)
		self.pbar = QtGui.QProgressBar(self)
		self.pbar.setRange(0, maxStep)
		self.pbar.setGeometry(30, 40, 200, 25)

		self.pbar.connect("valueChanged (int)", self.status)
		layout.addWidget(self.pbar)

		self.cBtn = QtGui.QPushButton("cancel")
		self.cBtn.connect('clicked()', lambda: self.cancelCopy())
		layout.addWidget(self.cBtn)
	
	def status(self):
		if self.pbar.value == self.pbar.maximum:
			self.close()
		
	def cancelCopy(self):
		self.pbar.value = self.pbar.maximum
		self.cancelCpy = True

def exportSelImgs():
	''' export the selected images to the given path '''
	if not mari.projects.current():
		mari.utils.message("No project currently open")
		return

	path = mari.utils.getExistingDirectory()
	if not os.path.exists(path):
		mari.utils.message("Not a valid path")
		return
	else:
		path = path + '/'

	images = mari.images.selected()

	if len(images) == 0:
		mari.utils.message("No images currently selected")
		return
	
	formats = [ str(i) for i in mari.images.supportedWriteFormats() ]

	maxStep = len( images )

	progressDiag = ProgressDialog(maxStep)
	progressDiag.show()

	progStep = 0
	for image in images:

		if progressDiag.cancelCpy == True:
			progressDiag.close()
			return

		imageName = ( image.filePath() ).split("/")[-1]

		try:
			format = imageName.split(".")[-1]

			# check if the format is valid...
			if format in formats:
				image.saveAs( path + imageName )
			else:
				format = ".tga"
				image.saveAs( path + imageName + format)
		except:
			pass

		progStep += 1
		progressDiag.pbar.setValue(progStep)

mari.menus.addAction(mari.actions.create('Export Images', 'exportSelImgs()'), 'MainWindow/Tools')
