# ------------------------------------------------------------------------------
# Merge Duplicate
# ------------------------------------------------------------------------------
# creates a merge duplicate of selected layers.	
# Same as Command+Shift+E / Ctrl+Shift+E in photoshop
# Will merge for selected patches other wise will merge all.
# Will rename the merged layer to the current active layer name + _mrgDup
# ** rename will work for mari 2.5 and after **
#
# copy the script to the same location as your log folder in 
# windows: C:\Users\[user_name]\Documents\Mari\Scripts
# linux: /home/[user_name]/Mari/Scripts
# Mac: /home/[Username]/Mari/Scripts
#
# Creates a menu item in Layers > Merge Duplicate 
# The default shortcut has been kept to ctrl+shift+E
# Which can be changed from Edit > shortcuts
#
# @uthor sreenivas alapati (cg-cnu)
# ------------------------------------------------------------------------------

from PySide import QtGui
import mari



def _isProjectSuitable():
    """Checks project state."""
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 20603300:
            return True, True

        return True, False
        
    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False, False



def clone_merge_layers(mode):
    ''' Creates a merge duplicate of selected layers - patch modes ALL or SELECTED'''
    
    suitable = _isProjectSuitable()
    if not suitable[0]:
          return

    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()
    curActiveLayerName = str(curChan.currentLayer().name())
    
    patches = list(curGeo.patchList())
    unSelPatches = [ patch for patch in patches if not patch.isSelected() ]
    
    mari.app.setWaitCursor()
    mari.history.startMacro('Clone & Merge Layers')

    copyAction = mari.actions.find('/Mari/Layers/Copy')
    copyAction.trigger()
    
    pasteAction = mari.actions.find('/Mari/Layers/Paste')
    pasteAction.trigger()
    
    curChan.mergeLayers()
    
    curLayer = curChan.currentLayer()

    if mode == 'selected':
        if len(patches) != len(unSelPatches):
        
            imgSet = curLayer.imageSet()
        
            for patch in unSelPatches:
                uv = patch.uvIndex()
                patchImg = imgSet.image(uv, -1)
                patchImg.fill(mari.Color(1,0,0,0))
    
        
    curLayer.setName(curActiveLayerName + '_mrgDup')
    mari.history.stopMacro()
    mari.app.restoreCursor()

    return


# ---------------------------------------------------------------


class CloneMergeGUI(QtGui.QDialog):
    '''GUI to select Clone Merge for selected patches or all patches'''

    def __init__(self):
        suitable = _isProjectSuitable()
        if suitable[0]:
            super(CloneMergeGUI, self).__init__()
            # Dialog Settings
            self.setFixedSize(300, 100)
            self.setWindowTitle('Clone & Merge Layers')
            # Layouts
            layoutV1 = QtGui.QVBoxLayout()
            layoutH1 = QtGui.QHBoxLayout()
            self.setLayout(layoutV1)
            # Widgets
            self.Descr =  QtGui.QLabel("Clone and merge selected layers for:")
            self.AllBtn = QtGui.QPushButton('All Patches')
            self.SelectedBtn = QtGui.QPushButton('Selected Patches')
            # Populate 
            layoutV1.addWidget(self.Descr)
            layoutV1.addLayout(layoutH1)
            layoutH1.addWidget(self.AllBtn)
            layoutH1.addWidget(self.SelectedBtn)
            # Connections
            self.AllBtn.clicked.connect(self.runCreateAll)
            self.SelectedBtn.clicked.connect(self.runCreateSelected)

    def runCreateSelected(self):
        clone_merge_layers('selected')
        self.close()

    def runCreateAll(self):
    	clone_merge_layers('none')
    	self.close()



###  Clone & merge layers UI Integration

UI_path = 'MainWindow/&Layers/'
script_menu_path = 'MainWindow/Scripts/Layers'

MergeDuplicate = mari.actions.create('Clone && Merge Layers', 'CloneMergeGUI().exec_()')
mari.menus.addAction(MergeDuplicate, UI_path,'Transfer')
mari.menus.addAction(MergeDuplicate, script_menu_path)

icon_filename = 'AddChannel.png'
icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
MergeDuplicate.setIconPath(icon_path)
MergeDuplicate.setShortcut('Ctrl+Shift+E')