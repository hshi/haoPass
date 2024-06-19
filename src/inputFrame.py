import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING
from src.auxiliary.pentry import PEntry

#===============
#PassFrame Class
#===============
class PassFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, master, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Init variables
		self.__initi_variables(master)

		#Create widgets
		self.__create_widgets()

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self, master):

		#master is the InputFrame
		self.master = master

		self.pass_len_var = tk.IntVar(value=12)
		self.contain_upper = tk.BooleanVar(value=True)
		self.contain_number = tk.BooleanVar(value=True)
		self.contain_special = tk.BooleanVar(value=True)

	#--------------
	#Create widgets
	#--------------
	def __create_widgets(self):

		#Set columns
		for i in [0,2,3,4,5]:
			self.columnconfigure(i, weight=1)

		#Set widgets
		oneButton = tk.Spinbox(self, from_=4, to=99, textvariable=self.pass_len_var, width=3)
		oneButton.grid(row = 0, column = 0, padx=(5, 0), pady=10, sticky='NSE')

		oneLabel = tk.Label(self, text="Characters")
		oneLabel.grid(row = 0, column = 1, padx=(0, 5), pady=10, sticky='NSW') 

		oneButton = tk.Checkbutton(self, text="Uppercase", variable=self.contain_upper)
		oneButton.grid(row = 0, column = 2, padx=5, pady=10, sticky='NS')

		oneButton = tk.Checkbutton(self, text="Number", variable=self.contain_number)
		oneButton.grid(row = 0, column = 3, padx=5, pady=10, sticky='NS')

		oneButton = tk.Checkbutton(self, text="Special", variable=self.contain_special)
		oneButton.grid(row = 0, column = 4, padx=5, pady=10, sticky='NS')

		oneButton = ttk.Button(self, text='Generate Password', command=self.generatePassword)
		oneButton.grid(row = 0, column = 5, padx=5, pady=10, ipadx=5, ipady=5, sticky='NS')

	#-----------------
	#Generate password
	#-----------------
	def generatePassword(self):

		#Read pass_len
		pass_len = self.__get_pass_len()

		#Define character pools
		lowercase_chars = string.ascii_lowercase
		uppercase_chars = string.ascii_uppercase
		digit_chars     = string.digits
		special_chars   = "`!@#$%^&*"

		#Some website can not recognize all specal characters.
		#special_chars  = string.punctuation

    #Ensure the password has at least one of each required character type if specified
		password = [ random.choice(lowercase_chars) ]
		if self.contain_upper.get():   password.append( random.choice(uppercase_chars) )
		if self.contain_number.get():  password.append( random.choice(digit_chars)     )
		if self.contain_special.get(): password.append( random.choice(special_chars)   )

		#Fill the rest of the password length with a mix of all character types
		all_chars = lowercase_chars
		if self.contain_upper.get():   all_chars += uppercase_chars
		if self.contain_number.get():  all_chars += digit_chars
		if self.contain_special.get(): all_chars += special_chars
		password += random.choices(all_chars, k=pass_len-len(password))

		#Shuffle the password list to avoid predictable patterns
		random.shuffle(password)

		#Get password
		password = ''.join(password)

		#Set password
		self.master.password_entry.pclear()
		self.master.password_entry.pinsert(0, password)

	#------------
	#Get pass_len
	#------------
	def __get_pass_len(self):

		try:
			pass_len = int( self.pass_len_var.get() )
			if pass_len<4: raise Exception("Password need to contain at least 4 characters!.")
		except Exception as e:
			pass_len=12; self.pass_len_var.set(12)
			showwarning(title='Warning', message=e)

		return pass_len

#==============================
#InputFrame Class -- Main Frame
#==============================
class InputFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Set styles
		self.set_styles()

		#Create Scrollbar Frame
		self.__create_scrollbar_frame()

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
		style.configure("InputFrame.ViewFrame.TFrame")
		style.configure("InputFrame.EditLable.TLabel",  anchor="center", background="#FFD700")

	#-----------------------------------------------------------------
	#Create the scrollbar frame, we pack other widget to the viewFrame
	#-----------------------------------------------------------------
	def __create_scrollbar_frame(self):

		#Create the canvas on the Frame
		self.mainCanvas = tk.Canvas(self)
		self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		#Attach the scrollbar to the canvas
		self.mainScrollbar = ttk.Scrollbar(self, orient='vertical', command=self.mainCanvas.yview)
		self.mainScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.mainCanvas['yscrollcommand'] = self.mainScrollbar.set
		self.mainCanvas.bind("<Configure>", self.__onCanvasConfigure)      
		self.mainCanvas.bind_all("<MouseWheel>", self._on_mousewheel)

		#Create the viewFrame on the canvas
		self.viewFrame = ttk.Frame(self.mainCanvas, style='InputFrame.ViewFrame.TFrame')
		self.mainCanvas.create_window((0,0), window=self.viewFrame, anchor=tk.NW, tags="InputFrame.viewFrame.Canvas")

	#----------------------------------------------------------------------
	#Change canvas and viewFrame size change with event -- when user resize
	#----------------------------------------------------------------------
	def __onCanvasConfigure(self, event):

		self.mainCanvas.itemconfigure("InputFrame.viewFrame.Canvas", width=event.width-4)
		self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all"))
		self.__update_scroll_state()

	#----------------------------------------------
	#Update Canvas -- when program add more widgets
	#----------------------------------------------
	def __updateFrameCanvas(self):

		self.mainCanvas.update_idletasks()
		self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all"))
		self.__update_scroll_state()

	#-------------------------------
	#Use mouse whell to scroll frame
	#-------------------------------
	def _on_mousewheel(self, event):

		#Only scroll if the content is taller than the canvas
		if self.content_too_tall:
			self.mainCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

	#-------------------
	#Update scroll state
	#-------------------
	def __update_scroll_state(self):

		# Calculate if the content is too tall for the canvas
		canvas_height = self.mainCanvas.winfo_height()
		content_height = self.mainCanvas.bbox("all")[3]
		self.content_too_tall = content_height > canvas_height

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self, container):

		#Input init
		self.container     = container

		#Account info init
		self.edit_label       = None

		self.account_label    = None
		self.account_entry    = None
		self.username_label   = None
		self.username_entry   = None
		self.password_label   = None
		self.password_entry   = None

		self.otherCombo_max   = 6
		self.otherCombo_label = []
		self.otherCombo_entry = []

		self.otherCombo_value = ["Email", "Phone", "Pin", "Address",  
														 "Security question 1", "Security question 2", "Security question 3", 
														 "Other"]

	#------------------
	#Create all widgets
	#------------------
	def __create_widgets(self):

		#Set Column
		for i in [0,1,2,3,4]:
			self.viewFrame.columnconfigure(i, weight=1)

		#Password Frame
		passFrame = PassFrame(self.viewFrame, self, borderwidth=2, relief="groove")
		passFrame.grid(row=0, column=0, columnspan=5, padx=15, pady=(15,5), sticky='NESW')

		#Top Buttons
		self.edit_label = ttk.Label(self.viewFrame, text= "New Account", style="InputFrame.EditLable.TLabel")
		self.edit_label.grid(row = 1, column = 0, padx=(15,5), pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Add Entry', command=self.__add_entry)
		oneButton.grid(row = 1, column = 1, padx=5, pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Remove Entry', command=self.__remove_entry)
		oneButton.grid(row = 1, column = 2, padx=5, pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Clear Entry', command=self.__clear_entry)
		oneButton.grid(row = 1, column = 3, padx=5, pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Submit', command=self.__submit_entry)
		oneButton.grid(row = 1, column = 4, padx=(5,15), pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		#Account Entry
		self.account_label = ttk.Combobox(self.viewFrame, values = ["Account"], justify="right", state="readonly")
		self.account_label.set("Account")
		self.account_label.grid(row = 2, column = 0, padx=(15,5), pady=(15,5), ipadx=5, ipady=5, sticky='NESW')

		self.account_entry = PEntry(self.viewFrame, "Required: it can be Website or App.")
		self.account_entry.grid(row = 2, column = 1, columnspan=4, padx=(5,15), pady=(15,5), ipadx=5, ipady=5, sticky='NESW')

		#Username Entry
		self.username_label = ttk.Combobox(self.viewFrame, values = ["Username"], justify="right", state="readonly")
		self.username_label.set("Username")
		self.username_label.grid(row = 3, column = 0, padx=(15,5), pady=5, ipadx=5, ipady=5, sticky='NESW')

		self.username_entry = PEntry(self.viewFrame, "Required: your account name or ID.")
		self.username_entry.grid(row = 3, column = 1, columnspan=4, padx=(5,15), pady=5, ipadx=5, ipady=5, sticky='NESW')

		#Password Entry
		self.password_label = ttk.Combobox(self.viewFrame, values = ["Password"], justify="right", state="readonly")
		self.password_label.set("Password")
		self.password_label.grid(row = 4, column = 0, padx=(15,5), pady=5, ipadx=5, ipady=5, sticky='NESW')

		self.password_entry = PEntry(self.viewFrame, "Required: your password.")
		self.password_entry.grid(row = 4, column = 1, columnspan=4, padx=(5,15), pady=5, ipadx=5, ipady=5, sticky='NESW')

		#Other Entry
		for i in range( len(self.otherCombo_entry), self.otherCombo_max ):

			self.otherCombo_label.append( ttk.Combobox(self.viewFrame, values=self.otherCombo_value, justify="right") )
			self.otherCombo_label[-1].grid(row = 5+i, column = 0, padx=(15,5), pady=5, ipadx=5, ipady=5, sticky='NESW')
		
			self.otherCombo_entry.append( PEntry(self.viewFrame, 'Optional: set any other information.') )
			self.otherCombo_entry[-1].grid(row = 5+i, column = 1, columnspan = 4, padx=(5,15), pady=5, ipadx=5, ipady=5, sticky='NESW')

	#----------------
	#Fresh LoginFrame
	#----------------
	def refresh(self):

		#Focus on container
		self.container.focus()

		#Some bind might be affected by other frames
		self.mainCanvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.container.unbind('<Return>')

	#---------
	#Add entry
	#---------
	def __add_entry(self):

		i = len(self.otherCombo_entry)

		self.otherCombo_label.append( ttk.Combobox(self.viewFrame, values=self.otherCombo_value, justify="right") )
		self.otherCombo_label[-1].grid(row = 5+i, column = 0, padx=(15,5), pady=5, ipadx=5, ipady=5, sticky='NESW')
		
		self.otherCombo_entry.append( PEntry(self.viewFrame, 'Optional: set any other information for your account.') )
		self.otherCombo_entry[-1].grid(row = 5+i, column = 1, columnspan = 4, padx=(5,15), pady=5, ipadx=5, ipady=5, sticky='NESW')

		self.__updateFrameCanvas()

	#------------
	#Remove entry
	#------------
	def __remove_entry(self):

		if( len(self.otherCombo_entry) == 0 ):
			showwarning( title='Warning', message="Deletion failed! The entry cannot be removed." )
			return
		
		self.otherCombo_label[-1].destroy()
		self.otherCombo_label.pop()

		self.otherCombo_entry[-1].destroy()
		self.otherCombo_entry.pop()

		self.__updateFrameCanvas()

	#-----------
	#Clear entry
	#-----------
	def __clear_entry(self):
		
		#Clear label
		self.edit_label.configure(text="New Account")

		#Clear basic
		self.account_entry.pclear()
		self.username_entry.pclear()
		self.password_entry.pclear()

		#Clear otherCombo
		for i in range( len(self.otherCombo_entry) ):
			self.otherCombo_label[i].delete(0, tk.END)
			self.otherCombo_entry[i].pclear()

	#------------
	#Submit entry
	#------------
	def __submit_entry(self):

		#Ask before submit
		answer = askokcancel( title='Confirmation', 
			                    message='Submit data to encrypted database?',
							            icon=WARNING
							          )
		if not answer: return

		#Init entry
		entry = {}

		#Read Account
		entry['Account']  = self.account_entry.pget()
		if( entry['Account'] == '' ): 
			showwarning( title='Warning', message="Account can not be empty!" )
			return

		#Read Username
		entry['Username'] = self.username_entry.pget()
		if( entry['Username'] == '' ): 
			showwarning( title='Warning', message="Username can not be empty!" )
			return

		#Read Password
		entry['Password'] = self.password_entry.pget()
		if( entry['Password'] == '' ): 
			showwarning( title='Warning', message="Password can not be empty!" )
			return

		#Read otherCombo
		for i in range( len(self.otherCombo_entry) ):

			#Read key and info
			key  = self.otherCombo_label[i].get().capitalize()
			info = self.otherCombo_entry[i].pget()

			#If Empty, continue
			if( key=='' and info==''):
				continue

			#Check for any error
			if( key=='' and info!=''):
				showwarning( title='Warning', message="Choose or input key for info: '{}'.".format(info) )
				return					
			if( key!='' and info==''):
				showwarning( title='Warning', message="Input information for key: '{}'.".format(key) )
				return			
			if( key in entry ):
				showwarning( title='Warning', message="Key '{}' can only be used once in the account!".format(key) )
				return				

			#Write into entry
			entry[key] = info

		#Write or update one account information
		try:
			label = self.edit_label.cget("text")
			if label == "New Account":
				m = self.container.db.write_one_account( entry )
				showinfo( title="Information", message=m )
			else:
				account_id = int( label.split(":")[1] )
				m = self.container.db.update_one_account( entry, account_id )
				showinfo( title="Information", message=m )

		except Exception as e:
			showwarning(title='Error', message=e)
			return

		#Clear entry after submit
		self.__clear_entry()

	#------------
	#Edit account
	#------------
	def edit_account(self, entry):

		#Get len_expect: min value is self.otherCombo_max
		len_expect  = max( len(entry)-4, self.otherCombo_max )

		#Make sure current length is expected
		len_current = len(self.otherCombo_entry)
		for i in range(len_current, len_expect): self.__add_entry()
		for i in range(len_expect, len_current): self.__remove_entry()

		#Clear entry
		self.__clear_entry()

		#Insert values
		#--label
		self.edit_label.configure(text="Edit Account: {}".format(entry["ID"]))
		#--required
		self.account_entry.pinsert( 0, entry["Account"] )
		self.username_entry.pinsert( 0, entry["Username"] )
		self.password_entry.pinsert( 0, entry["Password"] )
		#--others
		exclude_keys = ["ID", "Account", "Username", "Password"]
		other_entry  = {key: value for key, value in entry.items() if key not in exclude_keys}
		for i, (key, value) in enumerate(other_entry.items()):
			self.otherCombo_label[i].set(key)
			self.otherCombo_entry[i].pinsert(0, value)