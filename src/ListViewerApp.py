from Tkinter import *

class ListViewerApp:

	def __init__(self, root, vals):

		frame = Frame(root)
		frame.pack()
		
		self.label = Label(frame, text="Target Data:")
		self.label.grid(row=0,column=0, columnspan=1)

		self.listbox = Listbox(frame)

		for item in vals:
    			 self.listbox.insert(END,item)
		
		self.listbox.grid(row=1,column=0,columnspan=3)	

