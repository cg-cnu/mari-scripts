# ------------------------------------------------------------------------------
# Screenshot all channels
# Takes screenshot of all the channels in the current object
# Takes the path location and setting from view > screenshot settings
#
# Written by sreenivas alapati
# ------------------------------------------------------------------------------

import mari

def main():
    '''Creates snapshot of all the channels on the current object '''

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    chanList = curGeo.channelList()

    mari.app.setWaitCursor()

    for chan in chanList:
        chanName = str (chan.name())
        curGeo.setCurrentChannel(chan)
        curCanvas.repaint()

        snapAction = mari.action.find ('/Mari/Canvas/Take Screenshot')
        snapAction.trigger()

    curGeo.setCurrentChannel(curChannel)
    curCanvas.repaint()

    mari.app.restoreCursor()

mari.menus.addAction(mari.action.create('Screenshot all channels', 'main()'), "MainWindow/View")
