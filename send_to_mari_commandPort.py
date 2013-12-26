import mari

def enableCommandPort():

	mari.app.enableCommandPort( not mari.app.commandPortEnabled() )

	if mari.app.commandPortEnabled():
		print "command port enabled with the number", mari.app.commanPortNumber()
	else:
		print "command port disabled"

mari.menus.addAction(mari.actions.crete('Toggle Command Port', 'enableCommandPort()'), "MainWindow/Python")
