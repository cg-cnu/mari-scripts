# ------------------------------------------------------------------------------
# Channel Tools
# ------------------------------------------------------------------------------
# A bunch of tools to easy out some channel task
# 
# Delete multiple channels in one go.
#
# Copy the selected / all layers in the current channel to other channels as 
#		individual layers or as a single merged copy.
#
# Share current channel to other channels.
#
#
### TODO ###
# Export multiple Channels for all the selected patches
#
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menu item in Channels > Channel Tools
# 
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari
import PythonQt

GUI = PythonQt.QtGui
USER_ROLE = 32

def mergeDuplicate():
	''' create a merge duplicate of the selected layers'''

	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()

	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	pasteAction = mari.actions.find('/Mari/Layers/Paste')
	pasteAction.trigger()
	
	curChan.mergeLayers()
	
	return

def setChannelList():
	''' Updates the channels in the list - displays all the channels
	in all the objects except the current channel in current object'''
	
	global channelList

	channelList = []
	geoms = mari.geo.list()
	
	for geom in geoms:
		channels = geom.channelList()
		geomName = str (geom.name())
		
		for channel in channels:
			channelName = str (channel.name())
			channelList.append(geomName + '-->' + channelName)

	curGeo = mari.geo.current()
	curGeoName = str ( curGeo.name() )
	
	curChan = curGeo.currentChannel()
	curChanName = str ( curChan.name() )
	
	channelList.remove(curGeoName + '-->' + curChanName)
	channelListWidget.clear()
	
	for channel in channelList:
		channelListWidget.addItem(channel)
		channelListWidget.item(channelListWidget.count -1).setData(USER_ROLE, channel)

	return
	
def deleteMultipleChannels():
	''' Delete multiple channels in one go '''

	selectedChannelItems = channelListWidget.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mari.utils.message ('Select at least one channel to delete')
		return
	
	mari.history.startMacro('Delete Multi Channels ')
	for channel in selectedChannelItemsText:
		[ tmpObj, tmpChan ] = channel.split('-->')
		
		obj = mari.geo.get(tmpObj)
		chan = obj.channel(tmpChan)
		obj.removeChannel(chan)
		setChannelList()

	mari.history.stopMacro()

	return
	
def copyLayersToChannels():
	''' copy layers from current channel to other channels'''

	curGeo = mari.geo.current
	curChan = curGeo.currentChannel()
	layerList = list ( curChan.layerList() )
	
	selectedChannelItems = channelListWidget.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mai.utils.message( ' select at least one channel to copy ' )
		return
		
	mari.history.startMacro('Copy Layers To Channels')
	mari.app.setWaitCursor()
	
	if channelCopyCheck.isChecked():
		for layer in layerList:
			layer.setSelected(True)

	if mergeCheck.isChecked():
		mergeDuplicate()
		
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	if mergeCheck.isChecked():
		cur_chan.removeLayers()
	
	for i in selectedChannelItemsText:
		[ geo, chan ] = i.split('-->')
		
		try:
			mari.geo.setCurrent(geo)
			chan.makeCurrent(chan)
			pasteAction = mari.actions.find('/Mari/Layers/Paste')
			pasteAction.trigger()
			
		except AttributeError:
			pass
		
	mari.geo.setCurrent(curGeo)
	curGeo.setcurrent(curChan)

	mari.app.restoreCursor()	
	mari.history.stopMacro()
	
	return
		
def shareToChannel():
	''' Share current channel to selected channels in the list '''

	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()
	curChanName = str (curChan.name())
	
	selectedChannelItems = channelListWidget.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mai.utils.message( ' select at least one channel to copy ' )
		return
	
	mari.history.startMacro('Share Channel To Channels')
	
	for channel in selectedChannelItemsText:
		[ tmpObj, tmpChan ] = [ channel.split('-->') ] 
		
		tarObj = mari.geo.get(tmpObj)
		tarChan = tarObj.channel(tmpChan)
		tarChan.createChannelLayer(cur_chan_name, cur_chan)

	mari.history.stopMacro()
	
	return
	
channelDialog = GUI.QDialog()
channelDialog.setWindowTitle('Channel Tools')

vChannelLayout = GUI.QVBoxLayout()

channelDialog.setLayout(vChannelLayout)
channelDialog.setGeometry(800,200,600,800)

updatechanButton = GUI.QPushButton('Update Channels')
updatechanButton.connect('clicked()', lambda: setChannelList())
updatechanButton.setToolTip('Update the channel list')
vChannelLayout.addWidget(updatechanButton)

channelListWidget = GUI.QListWidget()
channelListWidget.setSelectionMode(channelListWidget.ExtendedSelection)
vChannelLayout.addWidget(channelListWidget)

deleteChannels = GUI.QPushButton('Delete')
deleteChannels.connect('clicked()', lambda: deleteMultipleChannels())
deleteChannels.setToolTip(' Delete the selected channels ')
vChannelLayout.addWidget(deleteChannels)

hChannelLayout = GUI.QHBoxLayout()

channelCopyCheck = GUI.QCheckBox('all layers')
channelCopyCheck.setToolTip('copy all the layers in the current channel')
hChannelLayout.addWidget(channelCopyCheck)

mergeCheck = GUI.QCheckBox('Merge')
mergeCheck.setToolTip('merge the layers')
hChannelLayout.addWidget(mergeCheck)

vChannelLayout.addLayout(hChannelLayout)

copyToChannelButton = GUI.QPushButton('Copy')
copyToChannelButton.connect('clicked()', lambda: copyLayersToChannels())
copyToChannelButton.setToolTip('copy the layers to the selected channels')
vChannelLayout.addWidget(copyToChannelButton)

shareToChannelButton = GUI.QPushButton('share')
shareToChannelButton.connect('clicked()', lambda: shareToChannels())
shareToChannelButton.setToolTip('share the current channel to the target channels ')
vChannelLayout.addWidget(shareToChannelButton)

def channelToolsUi():
	''' Show ui '''
	if mari.projects.current() is None:
		mari.utils.message('No project currently open')
		return
	channelDialog.show()

mari.menus.addAction(mari.actions.create('Channel Tools', 'channelToolsUi()'), "MainWindow/Channels")
