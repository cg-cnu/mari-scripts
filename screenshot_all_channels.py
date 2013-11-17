# ------------------------------------------------------------------------------
# Screenshot all channels
# ------------------------------------------------------------------------------
# Takes screenshot of all the channels for the current object
# Specify the path and setting in View > Screenshot Settings
# *IMP*: Keep incremental -> Enabled 
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Will create a menue item in view > Screenshot All Channels
#
# Written by sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

import mari

def screenshotAllChans():
    '''Creates snapshot of all the channels on the current object '''

    if mari.projects.current() == None:
        mari.utils.message("No project currently open")
        return

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    chanList = curGeo.channelList()
    curCanvas = mari.canvases.current()

    mari.app.setWaitCursor()

    for chan in chanList:
        chanName = str (chan.name())
        curGeo.setCurrentChannel(chan)
        curCanvas.repaint()

        snapAction = mari.actions.find ('/Mari/Canvas/Take Screenshot')
        snapAction.trigger()

    curGeo.setCurrentChannel(curChannel)
    curCanvas.repaint()

    mari.app.restoreCursor()

    return

mari.menus.addAction(mari.actions.create('Screenshot All Channels', 'screenshotAllChans()'), "MainWindow/View")