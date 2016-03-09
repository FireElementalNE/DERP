
# import the Tk stuff
from Tkinter import *

import data.DirectoryViewerApp

import os, sys

import DerpMom
import DerpMomDaemon
from DERPMOM_CONFIG import *

class DerpMomApp:


	# initialize the window for the applicaton
	def __init__(self, root):

		frame = Frame(root)
		frame.pack()

		self.start_button = Button(frame,text="Start",command=self.start)
		self.start_button.grid(row=0, column=0, columnspan=1)

		self.stop_button = Button(frame,text="Stop",command=self.stop)
		self.stop_button.grid(row=0, column=1, columnspan=1)

		self.gen_button = Button(frame,text="GenKeys",command=self.generateKeys)
		self.gen_button.grid(row=0,column=2,columnspan=1)

		self.quit_button = Button(frame,text="Quit",command=root.destroy)
		self.quit_button.grid(row=0,column=3,columnspan=1)

		self.data_button = Button(frame,text="Targets",command=self.viewTargetData)
		self.data_button.grid(row=0,column=4,columnspan=1)

	# start and instance of DerpMom
	def start(self):

		retval = os.fork()
		if retval == 0:
			daemon = DerpMomDaemon.DerpMomDaemon(DERPMOM_PIDFILE)
			daemon.start()
		else:
			#cat_cmd = "cat " + DERPMOM_PIDFILE
			#pid = os.system(cat_cmd)
			print "\nDerpMom started on port " + str(DERPMOM_PORT_NUM)  # + " with pid " + pid 

	# stop the instance of DerpMom
	def stop(self):
		try:
			kill_cmd = "kill `cat " + DERPMOM_PIDFILE  + "`"
			os.system(kill_cmd)
			os.remove(DERPMOM_PIDFILE)
			print "\nDerpMom killed"
		except OSError:
			print '\nNo DerpMOM running....'

	# generate the keys for DerpMom
	def generateKeys(self):

		keygen_cmd = "ssh-keygen -t rsa -f " + DERPMOM_RSA_PATH + " -q -N " + DERPMOM_RSA_PASSPHRASE
		os.system(keygen_cmd)
		print "DerpMom RSA keys created"

	def viewTargetData(self):

		window = Tk()
		window.title("Derpmom - Target Data")
		dirApp = data.DirectoryViewerApp.DirectoryViewerApp(window,DERPMOM_TARGET_DATA_DIR)
		window.mainloop()		

