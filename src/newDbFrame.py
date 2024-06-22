import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING
from src.myDatabase import createMyDataBase
from src.auxiliary.pentry import PEntry
from src.auxiliary.useful import normpath

#================
#NewDbFrame Class
#================
class NewDbFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Set styles
		self.set_styles()

		#Init variables
		self.__initi_variables(container)

		#Create widgets
		self.__create_widgets()

		#Fresh the frame
		self.refresh()

	#----------
	#set styles
	#----------
	def set_styles(self):

		style = ttk.Style()
		style.configure( "NewDbFrame.Alert.TLabel", anchor="center", foreground="white", 
																								background="black", font=("Helvetica", 12, "bold") )

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self, container):

		#Init variables
		self.container = container

		#Get default_dir
		self.default_dir      = normpath( os.getcwd()+"\\data" )

		#Value for entry
		self.db_dir_var       = tk.StringVar( value = self.default_dir ) 
		self.db_name_entry    = None
		self.new_pass_1_entry = None
		self.new_pass_2_entry = None

	#--------------
	#Create widgets
	#--------------
	def __create_widgets(self):

		#Set column
		self.columnconfigure(1, weight=1)

		#Information label
		oneLabel = ttk.Label(self, text= "For security purposes, please enter your password twice.", style="NewDbFrame.Alert.TLabel")
		oneLabel.grid(row = 0, column = 0, columnspan=2, padx = 5, pady = (40,25), sticky='NS')

		#For database dir
		oneButton = ttk.Button(self, text='Select Directory', command=self.__select_dir)
		oneButton.grid(row = 1, column = 0, padx = (20, 5), pady = 25, ipadx=5, ipady=5, sticky='W')

		oneEntry = ttk.Entry(self, textvariable=self.db_dir_var)
		oneEntry.config(state= "disabled")
		oneEntry.grid(row = 1, column = 1, padx = (5,20), pady = 25, ipadx=5, ipady=5, sticky='NESW')

		#For database name
		oneLabel = tk.Label(self, text="Database Name")
		oneLabel.grid(row = 2, column = 0, padx = (20, 5), pady = 25, ipadx=5, ipady=5, sticky='W')

		self.db_name_entry = PEntry(self, "Name for database, please do not include file extension.")
		self.db_name_entry.grid(row = 2, column = 1, padx = (5,20), pady = 25, ipadx=5, ipady=5, sticky='NESW')

		#For new password
		oneLabel = tk.Label(self, text="Password Once")
		oneLabel.grid(row = 3, column = 0, padx = (20, 5), pady = 25, ipadx=5, ipady=5, sticky='W')

		self.new_pass_1_entry = ttk.Entry(self, show="*")
		self.new_pass_1_entry.grid(row = 3, column = 1, padx = (5,20), pady = 25, ipadx=5, ipady=5, sticky='NESW')

		#For new password
		oneLabel = tk.Label(self, text="Password Twice")
		oneLabel.grid(row = 4, column = 0, padx = (20, 5), pady = 25, ipadx=5, ipady=5, sticky='W')

		self.new_pass_2_entry = ttk.Entry(self, show="*")
		self.new_pass_2_entry.grid(row = 4, column = 1, padx = (5,20), pady = 25, ipadx=5, ipady=5, sticky='NESW')

		#Create submit_button
		oneButton = ttk.Button(self, text='Submit', command=self.__submit)
		oneButton.grid(row = 5, column = 0, columnspan=2, padx =0, pady = 25, ipadx=0, ipady=5, sticky='NS')

	#----------------
	#Fresh LoginFrame
	#----------------
	def refresh(self):

		#Focus on container
		self.container.focus()

		#Some bind might be affected by other frames
		self.container.bind('<Return>', self.__submit)

	#---------------
	#Select database
	#---------------
	def __select_dir(self):

		db_dir = filedialog.askdirectory(initialdir=self.default_dir, title='Please choose the directory you wish to store database.')

		#Insert into the entry
		if db_dir!="": self.db_dir_var.set(db_dir)

	#----------------
	#When user submit
	#----------------
	def __submit(self, event=None):

		#Check database directory
		db_dir = self.db_dir_var.get()
		if db_dir == "":
			showwarning(title='Warning', message="The directory for database is empty.")
			return

		#Check database name
		db_name = self.db_name_entry.pget()
		if db_name == "":
			showwarning(title='Warning', message="The name of database is empty.")
			return

		#Chcek database file
		db_file = normpath( db_dir+"\\"+db_name+".db" )
		if os.path.exists(db_file):

			answer = askokcancel(title="Confirmation", 
													 message="The database exists in selected directory. Do you want to replace it?", 
													 icon=WARNING)

			if not answer: return

		#Check password
		new_pass_1 = self.new_pass_1_entry.get()
		new_pass_2 = self.new_pass_2_entry.get()

		if new_pass_1 != new_pass_2:
			showwarning(title='Warning', message="The passwords you entered are different. Please re-type your passwords.")
			return

		if new_pass_1 == "":
			showwarning(title='Warning', message="The passwords you entered are empty. Please re-type your passwords.")
			return

		#Disconnect db
		self.container.close_database()

		#Create new db      
		try:

			self.container.db = createMyDataBase(db_file, new_pass_1)
			self.container.loginFrame.db_file = db_file
			self.container.title( 'HaoPass: {}'.format(os.path.basename(db_file)) )
			showinfo( title="Information", message="Create new database successfully.")

			self.db_name_entry.pclear()
			self.new_pass_1_entry.delete(0, tk.END)
			self.new_pass_2_entry.delete(0, tk.END)

			self.container.raise_inputFrame()

		except Exception as e:
			showerror(title='Error', message=e)