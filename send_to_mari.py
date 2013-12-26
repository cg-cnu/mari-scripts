import os
import sys
from telnetlib import Telnet

connection = Telnet('localhost', 6100)

path = str(os.getcwd() + '/')
images = sys.argv[1:]

for image in images:
	message = "mari.images.load('" + path + image + "')"
	connection.write(message)
	connection.write("\x04")
tn.close()
