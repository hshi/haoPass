import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING
from src.auxiliary.pentry import PEntry

#==================
#AccountFrame Class
#==================
class AccountFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, master, root, index, entry, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Init variables
		self.__initi_variables(master, root, index, entry)

		#Create widgets
		self.__create_widgets()

	#----------------
	#Inital variables
	#----------------
	def __initi_variables(self, master, root, index, entry):

		#master is the InputFrame
		self.master = master

		#root the app frame
		self.root = root

		#count the number
		self.index = index

		#entry is the account info
		self.entry = entry

	#--------------
	#Create widgets
	#--------------
	def __create_widgets(self):

		#Set columns
		for i in range(4):
			self.columnconfigure(i, weight=1)

		#Create tree_info
		columns = ('Key', 'Value')
		self.tree_info = ttk.Treeview(self, columns=columns, show='headings', height=len(self.entry)-1, 
			                                  selectmode='browse', style="ViewFrame.Treeview")

		#Create heading
		self.tree_info.heading('Key',    text='Key',   anchor='center')
		self.tree_info.heading('Value',  text='Value', anchor='center')

		#Create column
		self.tree_info.column('Key',    anchor='w', width=120,  minwidth=80)
		self.tree_info.column('Value',  anchor='w', width=400,  minwidth=320)

		#Insert value
		for key, value in self.entry.items():
			if key != 'ID': self.tree_info.insert('', tk.END, values=(key, value))

		#Grid tree_info
		self.tree_info.grid(row=0, column=0, columnspan=4, padx=15, pady=(15,5), sticky=tk.NSEW)

		#Select first
		first_item = self.tree_info.get_children()[0]
		self.tree_info.selection_set( first_item )

		#Label
		m = "{}. ID {}".format(self.index, self.entry["ID"])
		onelabel = ttk.Label(self, text=m, style="ViewFrame.AccountFrame.TLabel")
		onelabel.grid(row = 1, column = 0, padx=(15,5), pady=(5,15), ipadx=0, ipady=0, sticky='NS')

		#Buttons
		oneButton = ttk.Button(self, text="Copy Selection", command=self.copy_selection)
		oneButton.grid(row = 1, column = 1, padx=5, pady=(5,15), ipadx=0, ipady=0, sticky='NS')

		oneButton = ttk.Button(self, text="Edit Account", command=self.edit_account)
		oneButton.grid(row = 1, column = 2, padx=5, pady=(5,15), ipadx=0, ipady=0, sticky='NS')

		oneButton = ttk.Button(self, text="Delete Account", command=self.delete_account)
		oneButton.grid(row = 1, column = 3, padx=(5,15), pady=(5,15), ipadx=0, ipady=0, sticky='NS')

		#Place horizontal line
		separator = ttk.Separator(self, orient="horizontal")
		separator.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)

	#--------------
	#Copy Selection
	#--------------
	def copy_selection(self):
		
		selected_item = self.tree_info.selection()

		if selected_item:

			item  =	self.tree_info.item(selected_item)
			value = item['values'][1]
			self.root.clipboard_clear()
			self.root.clipboard_append(value)

	#------------
	#Edit Account
	#------------
	def edit_account(self):

		self.root.inputFrame.edit_account(self.entry)
		self.root.raise_inputFrame()

	#--------------
	#Delete Account
	#--------------
	def delete_account(self):

		account_id = int( self.entry["ID"] )

		answer = askokcancel( 
							 title='Confirmation',
							 message='Do you want to delete the account with ID {}?'.format(account_id),
							 icon=WARNING)

		if answer:
			m = self.root.db.delete_one_account( account_id )
			self.master.fresh_page()
			showinfo( title="Information", message=m )

#===================
#NavigateFrame Class
#===================
class NavigateFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Set container
		self.container = container

		#Set widgets
		for i in [0,1,4,5]:
			self.columnconfigure(i, weight=1)

		oneButton = ttk.Button(self, text="Firt Page", command=self.container.first_page)
		oneButton.grid(row = 0, column = 0, padx=5, pady=5, ipadx=5, ipady=5, sticky='NESW')
		
		oneButton = ttk.Button(self, text="Previous Page", command=self.container.previous_page)
		oneButton.grid(row = 0, column = 1, padx=5, pady=5, ipadx=5, ipady=5, sticky='NESW')

		self.pageNumEntry = ttk.Entry(self, width=3, justify='center')
		self.pageNumEntry.grid(row = 0, column = 2, padx=(5,5), pady=5, ipadx=5, ipady=5, sticky='NSE')

		self.maxPageNumLabel = ttk.Label(self, style="ViewFrame.NavigateFrame.TLabel")
		self.maxPageNumLabel.grid(row = 0, column = 3, padx=(0,5), pady=5, ipadx=0, ipady=5, sticky='NESW')

		oneButton = ttk.Button(self, text="Next Page", command=self.container.next_page)
		oneButton.grid(row = 0, column = 4, padx=5, pady=5, ipadx=5, ipady=5, sticky='NESW')

		oneButton = ttk.Button(self, text="Last Page", command=self.container.last_page)
		oneButton.grid(row = 0, column = 5, padx=5, pady=5, ipadx=5, ipady=5, sticky='NESW')

		#Init page
		self.set_page(0,0)

	#--------
	#Set page
	#--------
	def set_page(self, page_num, max_page_num):

		#For page_num
		self.pageNumEntry.delete(0, tk.END)
		self.pageNumEntry.insert(0, page_num)

		#For max_page_num
		self.maxPageNumLabel.configure(text="/{} ".format(max_page_num))


#=============================
#ViewFrame Class -- Main Frame
#=============================
class ViewFrame(ttk.Frame):

	#-------
	#Initial
	#-------
	def __init__(self, container, auto_clean_min, *args, **kwargs):

		#Initial
		super().__init__(container, *args, **kwargs)

		#Set styles
		self.set_styles()

		#Create Scrollbar Frame
		self.__create_scrollbar_frame()

		#Init variables
		self.__initi_variables(container, auto_clean_min)

		#Create widgets
		self.__create_widgets()

	#----------
	#set styles
	#----------
	def set_styles(self):

		style = ttk.Style()
		style.configure("ViewFrame.ViewFrame.TFrame")
		style.configure("ViewFrame.AccountFrame.TLabel", background="white")
		style.configure("ViewFrame.NavigateFrame.TLabel", anchor="center", background="white")
		style.configure("ViewFrame.NavigateFrame.TFrame", background='lightgray')

		#For Treeview, Padding=(left, top, right, botton)
		style.configure( "ViewFrame.Treeview", padding=(5,0,0,5), font=("Roboto Mono",9) )

		#If we allow user to install font on their PC, use following
		# if "Roboto Mono" in tkfont.families():
		# 	style.configure( "ViewFrame.Treeview", padding=(5,0,0,5), font=("Roboto Mono",9) )
		# elif "Inconsolata" in tkfont.families():
		# 	style.configure( "ViewFrame.Treeview", padding=(5,0,0,5), font=("Inconsolata", 10) )
		# elif "Consolas" in tkfont.families():
		# 	style.configure( "ViewFrame.Treeview", padding=(5,0,0,5), font=("Consolas",10) )
		# else:
		# 	style.configure( "ViewFrame.Treeview", padding=(5,0,0,5) )


	#-----------------------------------------------------------------
	#Create the scrollbar frame, we pack other widget to the viewFrame
	#-----------------------------------------------------------------
	def __create_scrollbar_frame(self):

		#Create a frame for the canvas and navigation
		self.innerFrame = ttk.Frame(self)
		self.innerFrame.pack(fill=tk.BOTH, expand=True)

		#Create the canvas on the Frame
		self.mainCanvas = tk.Canvas(self.innerFrame)
		self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		#Attach the scrollbar to the canvas
		self.mainScrollbar = ttk.Scrollbar(self.innerFrame, orient='vertical', command=self.mainCanvas.yview)
		self.mainScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.mainCanvas['yscrollcommand'] = self.mainScrollbar.set
		self.mainCanvas.bind("<Configure>", self.__onCanvasConfigure)      
		self.mainCanvas.bind_all("<MouseWheel>", self._on_mousewheel)

		#Create the viewFrame on the canvas
		self.viewFrame = ttk.Frame(self.mainCanvas, style='ViewFrame.ViewFrame.TFrame')
		self.mainCanvas.create_window((0,0), window=self.viewFrame, anchor=tk.NW, tags="ViewFrame.viewFrame.Canvas")

	#----------------------------------------------------------------------
	#Change canvas and viewFrame size change with event -- when user resize
	#----------------------------------------------------------------------
	def __onCanvasConfigure(self, event):

		self.mainCanvas.itemconfigure("ViewFrame.viewFrame.Canvas", width=event.width-4)
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
	def __initi_variables(self, container, auto_clean_min):

		#Input init
		self.container     = container

		#View init
		self.account_entry  = None
		self.username_entry = None
		self.password_entry = None
		self.others_entry   = None
		self.accounts_info  = []

		#Navigation init
		self.num_per_page   = 6
		self.max_page_num   = -1
		self.page_num       = -1

		#Auto clean
		self.auto_timer        = None
		self.auto_clear_screen = auto_clean_min

	#------------------
	#Create all widgets
	#------------------
	def __create_widgets(self):

		#Set Column
		for i in [1,2,3,5,6,7]:
			self.viewFrame.columnconfigure(i, weight=1)

		self.num_per_page_var = tk.IntVar(value=6)
		oneButton = tk.Spinbox(self.viewFrame, from_=2, to=20, textvariable=self.num_per_page_var, width=2)
		oneButton.grid(row = 0, column = 0, padx=(15,0), pady=(15,5), ipadx=0, ipady=5, sticky='NSE')

		descrip_label = ttk.Label(self.viewFrame, text= " accounts/page")
		descrip_label.grid(row = 0, column = 1, padx=(0,5), pady=(15,5), ipadx=0, ipady=5, sticky='NSW')

		oneButton = ttk.Button(self.viewFrame, text='Clear Screen', command=self.clear_screen)
		oneButton.grid(row = 0, column = 2, columnspan=2, padx=5, pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Clear Entry', command=self.__clear_entry)
		oneButton.grid(row = 0, column = 4, columnspan=2, padx=5, pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		oneButton = ttk.Button(self.viewFrame, text='Search', command=self.fresh_page)
		oneButton.grid(row = 0, column = 6, columnspan=2, padx=(5,15), pady=(15,5), ipadx=5, ipady=5, sticky='NS')

		#Account Entry
		oneLabel = ttk.Label(self.viewFrame, text="Account:")
		oneLabel.grid(row = 1, column = 0, padx=(15,0), pady=(15,5), ipadx=5, ipady=5, sticky='NSE')

		self.account_entry = PEntry(self.viewFrame, "Input key words", use_font=True)
		self.account_entry.grid(row = 1, column = 1, columnspan=3, padx=(0,5), pady=(15,5), ipadx=5, ipady=5, sticky='NESW')

		#Username Entry
		oneLabel = ttk.Label(self.viewFrame, text="Username:")
		oneLabel.grid(row = 1, column = 4, padx=(5,0), pady=(15,5), ipadx=5, ipady=5, sticky='NSE')

		self.username_entry = PEntry(self.viewFrame, "Input key words", use_font=True)
		self.username_entry.grid(row = 1, column = 5, columnspan=3, padx=(0,15), pady=(15,5), ipadx=5, ipady=5, sticky='NESW')

		#Others Entry
		oneLabel = ttk.Label(self.viewFrame, text="Others:")
		oneLabel.grid(row = 2, column = 0, padx=(15,0), pady=(5,15), ipadx=5, ipady=5, sticky='NSE')

		self.others_entry = PEntry(self.viewFrame, "Input key words", use_font=True)
		self.others_entry.grid(row = 2, column = 1, columnspan=3, padx=(0,5), pady=(5,15), ipadx=5, ipady=5, sticky='NESW')

		#Password Entry
		oneLabel = ttk.Label(self.viewFrame, text="Password:")
		oneLabel.grid(row = 2, column = 4, padx=(5,0), pady=(5,15), ipadx=5, ipady=5, sticky='NSE')

		self.password_entry = PEntry(self.viewFrame, "Input key words", use_font=True)
		self.password_entry.grid(row = 2, column = 5, columnspan=3, padx=(0,15), pady=(5,15), ipadx=5, ipady=5, sticky='NESW')

		#Place horizontal line
		separator2 = tk.Frame(self.viewFrame, bd=10, relief='sunken', height=4)
		separator2.grid(row=3, column=0, columnspan=8, sticky='NESW')

		#Set info_label
		self.info_label = tk.Text(self.viewFrame, height=2, bg='black', fg='white', font=("Helvetica", 14), pady=10)
		self.info_label.tag_configure("center", justify="center")
		self.info_label.insert(tk.END, "Account Information Unavailable.\n", "center")
		self.info_label.insert(tk.END, "Enter keywords and click the search button to retrieve details.", "center")
		self.info_label.config(state="disabled")
		self.info_label.grid(row = 4, column = 0, columnspan=8, padx=0, pady=(100,5), sticky='NESW')
		
		#Create navigation frame
		self.naviFrame = NavigateFrame(self, style="ViewFrame.NavigateFrame.TFrame")
		self.naviFrame.pack(side=tk.BOTTOM, fill=tk.X)
		#naviFrame.place(relx=0.5, rely=0.99, anchor='s')

		#Init Bind 
		self.container.focus()		
		self.container.bind('<Return>', self.fresh_page)

	#----------------
	#Fresh LoginFrame
	#----------------
	def refresh(self):

		#Focus on container
		self.container.focus()

		#Some bind might be affected by other frames
		self.mainCanvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.container.bind('<Return>', self.fresh_page)

	#-----------
	#Start timer
	#-----------
	def start_timer(self):

		#Start new timer
		if self.auto_clear_screen>0:
			self.auto_timer = self.container.after( int(self.auto_clear_screen*60000), self.clear_screen )

	#----------
	#Stop timer
	#----------
	def stop_timer(self):

		#Remove previous timer
		if self.auto_timer is not None:
			self.container.after_cancel(self.auto_timer)
			self.auto_timer = None

	#-----------
	#Reset timer
	#-----------
	def reset_timer(self):

		self.stop_timer()
		self.start_timer()

	#------------
	#Clear screen
	#------------
	def clear_screen(self):

		self.stop_timer()

		self.__destroy_accounts_info()
		self.__grid_info_label()
		self.__updateFrameCanvas()

	#-----------
	#Clear entry
	#-----------
	def __clear_entry(self):

		self.account_entry.pclear()
		self.username_entry.pclear()
		self.password_entry.pclear()
		self.others_entry.pclear()

	#----------
	#Frish page
	#----------
	def fresh_page(self, event=None):

		self.num_per_page = self.__get_number_per_page()
		self.max_page_num = (self.__get_accounts_num()-1) // self.num_per_page
		self.page_num = self.__read_page_num()
		self.__bound_page_num()

		self.naviFrame.set_page(self.page_num+1, self.max_page_num+1)
		self.__update_account_info()

	#----------
	#First page
	#----------
	def first_page(self):

		self.num_per_page = self.__get_number_per_page()
		self.max_page_num = (self.__get_accounts_num()-1) // self.num_per_page
		self.page_num = 0
		self.__bound_page_num()

		self.naviFrame.set_page(self.page_num+1, self.max_page_num+1)		
		self.__update_account_info()

	#-------------
	#Previous page
	#-------------
	def previous_page(self):

		self.num_per_page = self.__get_number_per_page()
		self.max_page_num = (self.__get_accounts_num()-1) // self.num_per_page
		self.page_num = self.__read_page_num() - 1
		self.__bound_page_num()

		self.naviFrame.set_page(self.page_num+1, self.max_page_num+1)
		self.__update_account_info()

	#---------
	#Next page
	#---------
	def next_page(self):

		self.num_per_page = self.__get_number_per_page()
		self.max_page_num = (self.__get_accounts_num()-1) // self.num_per_page
		self.page_num = self.__read_page_num() + 1
		self.__bound_page_num()

		self.naviFrame.set_page(self.page_num+1, self.max_page_num+1)
		self.__update_account_info()

	#----------
	#First page
	#----------
	def last_page(self):

		self.num_per_page = self.__get_number_per_page()
		self.max_page_num = (self.__get_accounts_num()-1) // self.num_per_page
		self.page_num = self.max_page_num
		self.__bound_page_num()

		self.naviFrame.set_page(self.page_num+1, self.max_page_num+1)
		self.__update_account_info()

	#-----------------------------
	#Update account info to screen
	#-----------------------------
	def __update_account_info(self):

		#Clear screen first
		self.clear_screen()

		#Get accounts and grid
		accounts = self.__get_accounts()
		if len(accounts)!=0: 
			self.__ungrid_info_label()
			self.__set_accounts_info(accounts)
			self.__updateFrameCanvas()

		#Set timer to clear screen
		self.reset_timer()

	#--------------------
	#Destroy account info
	#--------------------
	def __destroy_accounts_info(self):

		#Loop from last to first
		len_account = len(self.accounts_info)
		for i in range(len_account-1, -1, -1):
			self.accounts_info[i].destroy()
			self.accounts_info.pop()

	#--------------------------
	#Set accounts_info and grid
	#--------------------------
	def __set_accounts_info(self, accounts):

		#Reset self.accounts_info and grid
		pre_index = self.page_num*self.num_per_page+1
		for i in range(len(accounts)):
			self.accounts_info.append( AccountFrame(self.viewFrame, self, self.container, i+pre_index, accounts[i]) )
			self.accounts_info[-1].grid(row=4+i, column=0, columnspan=8, sticky='NESW')

	#---------------
	#Grid info_label
	#---------------
	def __grid_info_label(self):

		#Grid info if it not there.
		if self.info_label.winfo_manager()!='grid':
			self.info_label.grid(row = 4, column = 0, columnspan=9, padx=2, pady=(100,5), sticky='NESW')

	#-----------------
	#Ungrid info_label
	#-----------------
	def __ungrid_info_label(self):

		#Remove info if it is grid
		if self.info_label.winfo_manager()=='grid':
			self.info_label.grid_forget()

	#-------------------
	#Get number per page
	#-------------------
	def __get_number_per_page(self):

		try:
			num_per_page= int( self.num_per_page_var.get() )
			if num_per_page<2 or num_per_page>20: 
				raise Exception("Choose a number of items between 2 and 20 to display per page.")
		except Exception as e:
			num_per_page=6; self.num_per_page_var.set(6)
			showwarning(title='Warning', message=e)
			return

		return num_per_page

	#-------------
	#Read page_num
	#-------------
	def __read_page_num(self):

		try:
			page_num = int( self.naviFrame.pageNumEntry.get() ) - 1
			return page_num

		except Exception as e:
			showwarning(title='Warning', message=e)
			return self.page_num
		
	#-----------------------------------------------------
	#Bound the self.page_num between 0 ~ self.max_page_num
	#-----------------------------------------------------
	def __bound_page_num(self):

		#If no items, set to -1 (show 0 on page number)
		if( self.max_page_num== -1 ):
			self.page_num = -1
			return

		#self.page_num must be between 0~max_page_num
		if( self.page_num > self.max_page_num ):
			self.page_num = self.max_page_num
			return

		elif( self.page_num < 0 ):
			self.page_num = 0
			return

	#--------------------
	#Get the accounts_num
	#--------------------
	def __get_accounts_num(self):

		accounts_num =  self.container.db.read_account_num_filter(
																	    account   = self.account_entry.pget(),
																	    username  = self.username_entry.pget(),
																	    password  = self.password_entry.pget(),
																	    others    = self.others_entry.pget() 
																		  )
		return accounts_num

	#--------------------------
	#Get accounts from database
	#--------------------------
	def __get_accounts(self):

		accounts = self.container.db.read_account_filter( row_count = self.num_per_page, 
																 offset    = self.page_num*self.num_per_page,
																 account   = self.account_entry.pget(),
																 username  = self.username_entry.pget(),
																 password  = self.password_entry.pget(),
																 others    = self.others_entry.pget() 
																)
		return accounts