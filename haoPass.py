import os
import datetime
import pyglet
pyglet.options['win32_gdi_font'] = True
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import askokcancel, WARNING
from tkinter.messagebox import showerror, showwarning, showinfo
from src.myDefault import MyDefault
from src.myDatabase import Mydb
from src.newDbFrame import NewDbFrame
from src.loginFrame import LoginFrame
from src.inputFrame import InputFrame
from src.viewFrame import ViewFrame
from src.tops.autoCleanTop import AutoCleanTop
from src.tops.autoLogoutTop import AutoLogoutTop
from src.tops.changePassTop import ChangePassTop
from src.tops.welcomeApp import WelcomeAppTop
from src.auxiliary.useful import normpath

#================
#Main tkintel App
#================
class App(tk.Tk):

	#---------------
	#Initial the App
	#---------------
	def __init__(self):

		#Initial
		super().__init__()

		#Set styles
		self.__set_styles()

		#Check app before run
		self.__check_app_files()

		#Init variables
		self.__initi_variables()

		#Set App info
		self.__set_App_info()

		#Create menubar
		self.__create_menubar()

		#Set frames
		self.__set_frames()

		#Init the timer
		self.init_timer()

	#----------
	#set styles
	#----------
	def __set_styles(self):

		#Use theme
		style = ttk.Style()
		style.theme_use("vista")		

		#Load fonts
		pyglet.font.add_file("fonts\\RobotoMono-Regular.ttf")
		
	#---------------
	#Check app files
	#---------------
	def __check_app_files(self):

		dirname = os.getcwd() + "\\data"
		if not os.path.exists(dirname): os.makedirs(dirname)

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self):

		#Get default
		self.default = MyDefault()

		#Database
		self.db = None

		#For timer init
		self.timer = None
		self.timeout_min = None

		#Current frame: monitor current frame
		self.current_frame = None

		#Frames
		self.loginFrame = None
		self.newDbFrame = None
		self.inputFrame = None
		self.viewFrame  = None

	#---------------
	#Inital App info
	#---------------
	def __set_App_info(self):

		#Set icon
		self.icon_image = tk.PhotoImage(file='images\\padlock.png')
		self.iconphoto(True, self.icon_image)

		#Set title
		self.title('HaoPass: None')

		#Set geometry
		w, h = self.default.get_win_size()   
		self.geometry('{}x{}'.format(w, h))

		#set other
		self.resizable(True, True)

		#Bind event
		self.protocol("WM_DELETE_WINDOW", self.on_close)

	#--------------
	#Create menubar
	#--------------
	def __create_menubar(self):

		#Init menubar
		self.menubar = tk.Menu(self)
		self.config(menu=self.menubar)

		#Create file_menu
		self.file_menu = tk.Menu(self.menubar, tearoff=0)
		self.file_menu.add_command(label='New', command=self.raise_newDbFrame)
		self.file_menu.add_command(label='Open', command=self.on_open)
		self.file_menu.add_command(label='Exit', command=self.on_close)
		self.menubar.add_cascade(label="File", menu=self.file_menu)

		#Create view_menu
		self.view_menu = tk.Menu(self.menubar, tearoff=0)
		self.view_menu.add_command(label='View Account', command=self.raise_viewFrame)
		self.view_menu.add_command(label='View Auto Clean', command=self.__view_autoclean)
		self.view_menu.add_command(label='View Auto Logout', command=self.__view_autologout)
		self.view_menu.add_command(label='View Default Screen', command=self.__reset_screen)
		self.menubar.add_cascade(label="View", menu=self.view_menu)

		#Create edit_menu
		self.edit_menu = tk.Menu(self.menubar, tearoff=0)
		self.edit_menu.add_command(label='Input Account', command=self.raise_inputFrame)
		self.edit_menu.add_command(label='Change Password', command=self.__change_password)
		self.edit_menu.add_command(label='Vacuum Data', command=self.__vacuum_db)
		self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

		#Create help_menu
		self.help_menu = tk.Menu(self.menubar, tearoff=0)
		self.help_menu.add_command(label='Welcome', command=self.__welcome_app)
		self.menubar.add_cascade(label="Help", menu=self.help_menu)

	#----------
	#Set Frames
	#----------
	def __set_frames(self):

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.loginFrame = LoginFrame(self, self.default.get_db_file())
		self.loginFrame.grid(row=0, column=0, sticky="NESW")

		self.newDbFrame = NewDbFrame(self)
		self.newDbFrame.grid(row=0, column=0, sticky="NESW")

		self.inputFrame = InputFrame(self)
		self.inputFrame.grid(row=0, column=0, sticky="NESW")

		self.viewFrame = ViewFrame(self, self.default.get_auto_clean())
		self.viewFrame.grid(row=0, column=0, sticky="NESW")

		#Raise frame
		if self.loginFrame.db_file == "": self.raise_newDbFrame()
		else: self.raise_loginFrame()

	#--------------------------------------------
	#Init timer: init value, bind and start timer
	#--------------------------------------------
	def init_timer(self):

		self.timer = None
		self.timeout_min = self.default.get_auto_logout()

		self.bind_all('<Any-KeyPress>', self.reset_timer)
		self.bind_all('<Any-Button>', self.reset_timer)
		self.bind_all('<Motion>', self.reset_timer)

		self.start_timer()

	#-----------
	#Start timer
	#-----------
	def start_timer(self):

		if self.timeout_min>0 and self.current_frame not in [self.loginFrame, self.newDbFrame]:
			self.timer = self.after( int(self.timeout_min*60000), self.raise_loginFrame )

	#----------
	#Stop timer
	#----------
	def stop_timer(self):

		if self.timer is not None:
			self.after_cancel(self.timer)
			self.timer=None

	#-----------
	#Reset timer
	#-----------
	def reset_timer(self, event=None):

		self.stop_timer()
		self.start_timer()

	#----------------
	#Raise loginFrame
	#----------------
	def raise_loginFrame(self, db_file=None):

		#Close self.db
		self.close_database()

		#Clear screen on viewFrame
		self.viewFrame.clear_screen()

		#Raise the frame
		self.loginFrame.refresh(db_file)
		self.loginFrame.tkraise()
		self.current_frame = self.loginFrame

	#----------------
	#Raise newDbFrame
	#----------------
	def raise_newDbFrame(self):

		self.newDbFrame.refresh()
		self.newDbFrame.tkraise()
		self.current_frame = self.newDbFrame

	#----------------
	#Raise inputFrame
	#----------------
	def raise_inputFrame(self):

		#Do not raise if no database
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		#Raise the frame
		self.inputFrame.refresh()
		self.inputFrame.tkraise()
		self.current_frame = self.inputFrame

	#---------------
	#Raise viewFrame
	#---------------
	def raise_viewFrame(self):

		#Do not raise if no database
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		#Raise the frame
		self.viewFrame.refresh()
		self.viewFrame.tkraise()
		self.current_frame = self.viewFrame

	#----------------------
	#Open the autoclean top
	#----------------------
	def __view_autoclean(self):

		#Do not raise if db is not set
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		autoCleanTop = AutoCleanTop(self)
		autoCleanTop.grab_set()

	#-----------------------
	#Open the autologout top
	#-----------------------
	def __view_autologout(self):

		#Do not raise if db is not set
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		autoLogoutTop = AutoLogoutTop(self)
		autoLogoutTop.grab_set()

	#-----------------------
	#Open the changePass top
	#-----------------------
	def __change_password(self):

		#Do not raise if db is not set
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		changePassTop = ChangePassTop(self)
		changePassTop.grab_set()

	#--------------------
	#Open the welcome app
	#--------------------
	def __welcome_app(self):

		welcomeAppTop = WelcomeAppTop(self)
		welcomeAppTop.grab_set()

	#-----------------------
	#Reset screen to default
	#-----------------------
	def __reset_screen(self):

		w, h = self.default.get_default_win_size()
		self.geometry('{}x{}'.format(w, h))
		self.update()

	#----------------
	#Vacuum data base
	#----------------
	def __vacuum_db(self):

		#Do not vacuum if db is not set
		if self.db is None: 
			showwarning(title='Warning', message="Database connection not found.")
			return 

		command_sql = "VACUUM;"
		lastrowid = self.db.commit_command(command_sql)

		showinfo( title='Information', message='Vacuumed the database.')

	#----------------------------------
	#Open database and raise loginframe
	#----------------------------------
	def on_open(self):

		#Open the file dialog to select a file
		db_file = filedialog.askopenfilename(
												 initialdir=normpath( os.getcwd()+"\\data" ),
		                     title="Select a File",
		                     filetypes=(("database", "*.db"), ("All files", "*.*"))
		                     )

		#Raise loginframe depends on db_file
		if db_file != "": self.raise_loginFrame(db_file)

	#-----------------------
	#Bind to the close event 
	#-----------------------
	def on_close(self):

		#Stop timer
		self.stop_timer()
		self.viewFrame.stop_timer()

		#Save default
		self.__save_default()

		#Close connection
		self.close_database()

		#Destroy 
		self.destroy()

	#--------------
	#Close database
	#--------------
	def close_database(self):

		if( self.db is not None ): 
			self.db.disconnect()
			self.db = None
			self.title('HaoPass: None')

	#----------------
	#Save the history
	#----------------
	def __save_default(self):

		self.default.update_win_size( self.winfo_width(), self.winfo_height() )
		self.default.update_auto_clean( self.viewFrame.auto_clear_screen )
		self.default.update_auto_logout( self.timeout_min )
		self.default.update_database_file( self.loginFrame.db_file )
		self.default.save()

	#----------------------------
	#Define my callback exception
	#----------------------------
	def report_callback_exception(self, exc, val, tb):

		# 'exc' is the exception type, 'val' is the exception value, 'tb' is the traceback
		m = "{}\n{}".format(exc, val)
		showerror(title='Error', message=m)
		self.on_close()

#=========
#Main code
#=========
if __name__ == "__main__":

	app = App()
	app.mainloop()