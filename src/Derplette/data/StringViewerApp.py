from Tkinter import *

class StringViewerApp:

	def __init__(self, root, s):

		self.string = s

		frame = Frame(root)
		frame.pack()

		self.label = Label(frame, text=s)
		self.label.pack()

		
