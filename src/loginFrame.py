import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from src.myDatabase import Mydb
from src.auxiliary.useful import normpath

#================
#LoginFrame Class
#================
class LoginFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, db_file, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Set styles
		self.set_styles()
		
		#Init variables
		self.__initi_variables(container, db_file)

		#Create widgets
		self.__create_widgets()
		
		#Fresh the frame
		self.refresh()

	#----------
	#set styles
	#----------
	def set_styles(self):

		style = ttk.Style()
		style.configure( "LoginFrame.Alert.TLabel", anchor="center", foreground="white", 
																								background="black", font=("Helvetica", 12, "bold") )

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self, container, db_file):

		#Input init
		self.container    = container

		#Set self.db_file: final value, will be updated after submit button
		self.db_file = normpath(db_file)
		if not os.path.exists(self.db_file): self.db_file = ""

		#Get default_dir
		self.default_dir  = normpath( os.getcwd()+"\\data" )

		#Value for entry
		self.db_file_var    = tk.StringVar() #only store value in entry
		self.password_var   = tk.StringVar() #store password
		self.password_entry = None

	#--------------
	#Create widgets
	#--------------
	def __create_widgets(self):

		#Set column
		self.columnconfigure(1, weight=1)

		#Information label
		oneLabel = ttk.Label(self, text= "Please input the password for selected database.", style="LoginFrame.Alert.TLabel")
		oneLabel.grid(row = 0, column = 0, columnspan=2, padx = 5, pady = (80,40), sticky='NS')

		#For database path
		oneButton = ttk.Button(self, text='Select database', command=self.__select_database)
		oneButton.grid(row = 1, column = 0, padx = (20, 5), pady = 40, ipadx=5, ipady=5, sticky='W')

		oneEntry = ttk.Entry(self, textvariable=self.db_file_var)
		oneEntry.config(state= "disabled")
		oneEntry.grid(row = 1, column = 1, padx = (5,20), pady = 40, ipadx=5, ipady=5, sticky='NESW')

		#For password
		oneLabel = ttk.Label(self, text= "Enter Password: ")
		oneLabel.grid(row = 2, column = 0, padx = (20, 5), pady = 40, ipadx=5, ipady=5, sticky='W')

		self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
		self.password_entry.grid(row = 2, column = 1, padx = (5,20), pady = 40, ipadx=5, ipady=5, sticky='NESW')

		#Create submit_button
		oneButton = ttk.Button(self, text='Submit', command=self.__submit)
		oneButton.grid(row = 3, column = 0, columnspan=2, padx =0, pady = 40, ipadx=0, ipady=5, sticky='NS')

	#----------------
	#Fresh LoginFrame
	#----------------
	def refresh(self, db_file=None):

		#Update self.db_file_var
		if db_file is not None: self.db_file_var.set(db_file) 
		else: self.db_file_var.set(self.db_file) 

		#Focus on password_entry
		self.password_entry.focus_set()
		
		#Some bind might be affected by other frames
		self.container.bind('<Return>', self.__submit)

	#---------------
	#Select database
	#---------------
	def __select_database(self):

		#Open the file dialog to select a file
		db_file = filedialog.askopenfilename(
												 initialdir=self.default_dir,
												 title="Select a File",
												 filetypes=( ("database", "*.db"), ("All files", "*.*") )
												 )

		#Insert into the entry
		if db_file!="": self.db_file_var.set(db_file)

	#----------------
	#When user submit
	#----------------
	def __submit(self, event=None):

		try:

			#Disconnect db (after we change password on tk.Toplevel, self.container.db might not be None)
			self.container.close_database()

			#Connect to db
			db_file  = self.db_file_var.get()
			password = self.password_var.get()

			self.db_file = db_file
			self.container.db =Mydb(db_file, password)
			self.container.title( 'HaoPass: {}'.format(os.path.basename(db_file)) )

			showinfo( title="Information", message="Connected to the database successfully.")

			self.password_var.set("")
			self.container.raise_viewFrame()

		except Exception as e:

			m = "Unable to connect. Please ensure your credentials are correct and try again."
			showerror(title='Error', message=m)
