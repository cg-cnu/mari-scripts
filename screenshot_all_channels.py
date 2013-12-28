# ------------------------------------------------------------------------------
# Screenshot all channels
# ------------------------------------------------------------------------------
# Takes screenshot of all the channels for the current view.
# Specify the path and setting in View > Screenshot Settings.
# *IMP*: Keep incremental -> Enabled
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# a menue item in view > Screenshot All Channels will be created.
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari

def screenshotAllChannels():
    '''Take screenshot of all the channels for the current view '''

    if mari.projects.current() == None:
        mari.utils.message("No project currently open", title = "Error")
        return

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    chanList = curGeo.channelList()
    curCanvas = mari.canvases.current()

    mari.app.setWaitCursor()

    for chan in chanList:
        
        curGeo.setCurrentChannel(chan)
        curCanvas.repaint()
        
        snapAction = mari.actions.find ('/Mari/Canvas/Take Screenshot')
        snapAction.trigger()

    curGeo.setCurrentChannel(curChannel)
    curCanvas.repaint()
    
    mari.app.restoreCursor()

    return

mari.menus.addAction(mari.actions.create('Screenshot All Channels', 
						'screenshotAllChannels()'), "MainWindow/View")
