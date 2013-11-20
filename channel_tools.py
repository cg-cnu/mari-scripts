# Channel Tools
#
#
#
#

import mari
import PythonQt

GUI = PythonQt.QtGui
USER_ROLE = 32

def merge_duplicate():
	''' create a merge duplicate of the selected '''

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
	in all the objects except the current one'''
	
	channelList = []
	objs = mari.geo.list()
	
	for obj in objs:
		channels = obj.channelList()
		objName = str (obj.name())
		
		for channel in channels:
			channelName = str (channel.name())
			channelList.append(objName + '--' + channelName)

	curGeo = mari.geo.current()
	curGeoName = str ( curGeo.name() )
	curChan = curGeo.currentChannel()
	curChanName = str ( curChan.name() )
	
	channelList.remove(curGeoName + '--' + curChanName)
	
	channelListWidget.clear()
	
	for channel in channelList:
		channelListWidget.addItem(channel)
		channelListWidget.item(channelListWidget.count -1).setData(USER_ROLE, channel)

	return
	
def deleteMultiChannels():
	selectedChannelItems = channel_list.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mari.utils.message ('Select at least one channel to delete')
		return
	
	mari.history.startMacro('Delete Multi Channels ')
	for channel in selectedChannelItemsText:
		tmp_obj = channel.split('--')[0]
		tmp_chan = channel.split('--')[1]
		
		obj = mari.geo.get(tmp_obj)
		chan = obj.channel(tmp_chan)
		obj.removeChannel(chan)
		setChannelList()
	mari.history
	retun 
	
def copyLayersToChannels():
	curGeo = mari.geo.current
	curChan = curGeo.currentChannel()
	allLayers = list ( curChan.layerList() )
	
	selectedChannelItems = channel_list.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mai.utils.message( ' select at least one channel to copy ' )
		return
		
	mari.history.startMacro('Copy Layers To Channels')
	mari.app.setWaitCursor()
	
	if channelCopyCheck.isChecked()"
		for layer in layers:
			layer.setSelected(True)
			
	if mergeCheck.isChecked():
		merge_duplicate()
		
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	if mergeCheck.isChecked():
		cur_chan.removeLayers()
	
	for i in selectedChannelItemsText:
		tmp - i.split('--')
		geo = mari.geo.find(tmp[0])
		chan = geo.findChannel(tmp[1])
		
		try:
			mari.geo.setCurrent(geo)
			chan.makeCurrent()
			pasteAction = mari.actions.find('/Mari/Layers/Paste')
			pasteAction.trigger()
			
		except AttributeError:
			pass
		
	mari.geo.setCurrent(curGeo)
	curGeo.setcurrent(curChan)
	
	mari.history.stopMacro()
	mari.app.restoreCursor()
	
	return
		
def shareToChannel():

	curGeo = mari.geo.current()
	curChan = curGeo.currentChannel()
	curChanName = str (curChan.name())
	
	selectedChannelItems = channel_list.selectedItems()
	selectedChannelItemsText = [i.text() for i in selectedChannelItems ]
	
	if len(selectedChannelItemsText) == 0:
		mai.utils.message( ' select at least one channel to copy ' )
		return
	
	mari.history.startMacro('share channel To Channels')
	
	for channel in selectedChannelItemsText:
		tmp_obj = channel.split('--')[0]
		tmp_chan = channel.split('--')[1]
		
		tar_obj = mari.geo.get(tmp_obj)
		tar_chan = tar_obj.channel(tmp_chan)
		tar_chan.createChannelLayer(cur_chan_name, cur_chan)

	mari.history.stopMacro()
	
	return
	
channelDialog = GUI.QDialog()
channelDialog.setWindowTitle('Channel Tools')

vChannelLayout = GUI.QVBoxLayout()

channelDialog.setLayout()
channelDialog.setGeometry()

updatechanButton = GUI.QPushBUtton()
updatechanButton.connect('clicked()', lambda: setChannelList())
updatechanButton.setToolTip()
vChannelLayout.addWidget(updatechanButton)

channelListWidget = GUI.QListWidget()
channelListWidget.setSelectionMode(channel_list.ExtendedSelection)
vChannelLayout.addWidget(channelListWidget)

deleteChannels = GUI.QPushButton('Delete')
deleteChannels.connect('clicked()', lambda: deleteMultipleChannels())
deleteChannels.setToolTip(' flkjf ')
vChannelLayout.addWidget(deleteChannels)

channelCopyCheck = GUI.QCheckBox('all layers')
channelCopyCheck.setToolTip('copy all the layers in the current channel')
vChannelLayout.addWidget(channelCopyCheck)

mergeCheck = GUI.QCheckBox('Merge')
mergeCheck.setToolTip('merge the layers')
vChannelLayout.addWidget(mergeCheck)

copyToChannelButton = GUI.QPushButton('Copy')
copyToChannelButton.connect('clicked()', lambda: copyLayersToChannels())
copyToChannelButton.setToolTip('copy the selected layer to the selected channels')
vChannelLayout.addWidget(copyToChannelButton)

shareToChannelButton = GUI.QPushButton('share')
shareToChannelButton.connect('clicked()', lambda: shareToChannels())
shareToChannelButton.setToolTip('share the selected channel to the target channels ')
vChannelLayout.addWidget(shareToChannelButton)
	
def channelToolsUi():
	''' Show ui '''
	if mari.projects.current() is None:
		mari.utils.message('No project currently open')
		return
	channelDialog.show()

mari.menus.addAction(mari.actions.create('Channel Tools', 'channelToolsUi()'), "MainWindow/Channels")
	
