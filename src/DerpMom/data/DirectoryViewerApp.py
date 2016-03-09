from Tkinter import *

import os, sys
import TargetData

import StringViewerApp

class DirectoryViewerApp:

	def __init__(self, root, directory):

		self.directory = directory

		frame = Frame(root)
		frame.pack()
		
		self.label = Label(frame, text="Target Data:")
		self.label.grid(row=0,column=0, columnspan=1)

		self.listbox = Listbox(frame)

		dirList=os.listdir(directory)
		for fname in dirList:
			if '.html' not in fname and '.xml' not in fname: 
				self.listbox.insert(END,fname)
		
		self.listbox.grid(row=1,column=0,columnspan=3)	

		self.button = Button(frame, text="View Data", command=self.viewTarget)
		self.button.grid(row=2,column=0,columnspan=1)

	def viewTarget(self):

		ip = self.listbox.get(self.listbox.curselection()[0])
		
		td = TargetData.TargetData()

		print td.toString()		

		td.unserializeFromFile(str(ip),str(self.directory))
	
		tdstring = td.toString()

		print tdstring

		window = Tk()
		window.title("Target Data: " + str(ip))
		strApp = StringViewerApp.StringViewerApp(window,tdstring)
		window.mainloop()	
