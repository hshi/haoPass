import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

#----------------------
#Entry with Placeholder
#----------------------
class PEntry(ttk.Entry):

	#----
	#Init
	#----
	def __init__(self, container, placeholder="", use_font=False, *args, **kwargs):

		super().__init__(container, *args, **kwargs)

		#Set styles
		self.set_styles()

		#Set font
		if use_font: self.set_font()

		#Init variables
		self.placeholder = placeholder
		
		#Put pacehold
		self.put_placeholder()

		#Bind functions
		self.bind("<FocusIn>", self.on_focus_in)
		self.bind("<FocusOut>", self.on_focus_out)

	#----------
	#set styles
	#----------
	def set_styles(self):

		style = ttk.Style()
		style.configure('Placeholder.TEntry', padding=(5,0), foreground='grey')
		style.configure('PEntryText.TEntry', padding=(5,0), foreground='black')

	#--------
	#Set font
	#--------
	def set_font(self):

		self.configure( font=("Roboto Mono",9) )

		#If we allow user to install font on their PC, use following
		# if "Roboto Mono" in tkfont.families():
		# 	self.configure( font=("Roboto Mono",9) )
		# elif "Inconsolata" in tkfont.families():
		# 	self.configure( font=("Inconsolata", 10) )
		# elif "Consolas" in tkfont.families():
		# 	self.configure( font=("Consolas",10) )
		# else:
		# 	pass

	#---------------
	#Put placeholder
	#---------------
	def put_placeholder(self):

		self.insert(0, self.placeholder)
		self.configure(style='Placeholder.TEntry')

	#-----------
	#on focus in
	#-----------
	def on_focus_in(self, event):

		if self.get()==self.placeholder and self.cget("style")=='Placeholder.TEntry':
			self.delete(0, tk.END)
			self.configure(style='PEntryText.TEntry')

	#------------
	#on focus out
	#------------
	def on_focus_out(self, event):

		if not self.get():
			self.put_placeholder()

	#---------------
	#Placeholder get
	#---------------
	def pget(self):

		c = self.get()
		if c==self.placeholder and self.cget("style")=='Placeholder.TEntry':
			return ""
		else:
			return c

	#------------------
	#Placeholder insert
	#------------------
	def pinsert(self, index, string):

		self.on_focus_in(event=None)
		self.insert(index, string)

	#-----------------
	#Placeholder clear
	#-----------------
	def pclear(self):

		self.delete(0, tk.END)
		self.put_placeholder()


#=============
#Example usage
#=============
if __name__ == "__main__":

	root = tk.Tk()

	entry_with_placeholder_1 = PEntry(root, placeholder="Enter", use_font=True)
	entry_with_placeholder_1.pack(pady=10, padx=10)

	entry_with_placeholder_2= PEntry(root, placeholder="Enter A", use_font=True)
	entry_with_placeholder_2.pack(pady=10, padx=10)

	def read_1():
		c = entry_with_placeholder_1.pget()
		print( "read: {}".format(c)  )
	ttk.Button(root, text='read 1', command=read_1).pack()

	def clear_1():
		entry_with_placeholder_1.pclear()
	ttk.Button(root, text='clear 1', command=clear_1).pack()

	def insert_1():
		entry_with_placeholder_1.pinsert(0, "haha")
	ttk.Button(root, text='insert 1', command=insert_1).pack()

	root.mainloop()