import mari

def toggleCommandPort():

	mari.app.enableCommandPort( not mari.app.commandPortEnabled() )

	if mari.app.commandPortEnabled():
		print "command port enabled with the number", mari.app.commandPortNumber()
	else:
		print "command port disabled"

mari.menus.addAction(mari.actions.create('Toggle Command Port', 'toggleCommandPort()'), "MainWindow/Python")
