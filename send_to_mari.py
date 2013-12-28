#!/usr/bin/python
from telnetlib import Telnet
import sys

try:
	connection = Telnet('localhost', 6100)
	#message = "mari.projects.current()\x04"
	#connection.write(message)
	#reply = connection.read()
	#if reply:
	images = sys.argv[1:]

	for image in images:

		message = "mari.images.load('" + image + "')"
		connection.write(message)
		connection.write("\x04")

	connection.close()

except:
	import Tkinter
	import tkMessageBox
	window = Tkinter.Tk()
	window.wm_withdraw()
	tkMessageBox.showerror(title = 'Mari Error',
							message = 'Enable command port in mari')
							
