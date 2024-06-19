import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING
from src.myDatabase import Mydb

#==============================
#Top level Class: ChangePassTop
#==============================
class ChangePassTop(tk.Toplevel):

  #-------
  #Initial
  #-------
  def __init__(self, container, *args, **kwargs):

    #Initial
    super().__init__(container, *args, **kwargs)

    #Init variables
    self.__initi_variables(container)

    #Init the info for top
    self.__init_top_info()

    #Create widgets
    self.__create_widgets()

  #----------------
  #Inital variables
  #----------------
  def __initi_variables(self, container):

    #Init variables
    self.container = container

  #---------------------
  #Init the info for top
  #---------------------
  def __init_top_info(self):

    w, h = 450, 280
    x, y = self.container.winfo_x(), self.container.winfo_y()
    self.geometry( "%dx%d+%d+%d" %(w,h,x+50,y+50) )
    self.title('Change Password')

    #Define custom close function
    self.protocol("WM_DELETE_WINDOW", self.on_close)

  #--------------
  #Create widgets
  #--------------
  def __create_widgets(self):

    #Set column
    self.columnconfigure(1, weight=1)

    #Information label
    oneLabel = ttk.Label(self, text= "For security purposes, please enter your new password twice. ")
    oneLabel.grid(row = 0, column = 0, columnspan=2, padx = 5, pady = 25, sticky='NS')

    #For old password
    oneLabel = tk.Label(self, text="Current Password:")
    oneLabel.grid(row = 1, column = 0, padx = (15,5), pady = 5, ipadx=5, ipady=5, sticky='NSW') 

    self.pre_pass_entry = ttk.Entry(self)
    self.pre_pass_entry.grid(row = 1, column = 1, padx = (5,15), pady = 5, ipadx=5, ipady=5, sticky='NESW')

    #For new password
    oneLabel = tk.Label(self, text="New Password 1:")
    oneLabel.grid(row = 2, column = 0, padx = (15,5), pady = (15,5), ipadx=5, ipady=5, sticky='NSW') 

    self.new_pass_1_entry = ttk.Entry(self, show="*")
    self.new_pass_1_entry.grid(row = 2, column = 1, padx = (5,15), pady = (15,5), ipadx=5, ipady=5, sticky='NESW')

    #For new password
    oneLabel = tk.Label(self, text="New Password 2:")
    oneLabel.grid(row = 3, column = 0, padx = (15,5), pady = (15,5), ipadx=5, ipady=5, sticky='NSW') 

    self.new_pass_2_entry = ttk.Entry(self, show="*")
    self.new_pass_2_entry.grid(row = 3, column = 1, padx = (5,15), pady = (15,5), ipadx=5, ipady=5, sticky='NESW')

    #Create submit_button
    oneButton = ttk.Button(self, text='Submit', command=self.__submit)
    oneButton.grid(row = 4, column = 0, columnspan=2, padx =0, pady = 15, ipadx=5, ipady=5, sticky='NS')

    #Focus and bind
    self.pre_pass_entry.focus_set()    
    self.bind('<Return>', self.__submit)

  #----------------
  #When user submit
  #----------------
  def __submit(self, event=None):

    #Read new password
    new_pass_1 = self.new_pass_1_entry.get()
    new_pass_2 = self.new_pass_2_entry.get()

    #Check if they are the same
    if new_pass_1 != new_pass_2:
      showwarning(title='Warning', message="The new passwords you entered are different. Please re-type your new passwords.")
      return

    if new_pass_1 == "":
      showwarning(title='Warning', message="The new passwords you entered are empty. Please re-type your new passwords.")
      return

    #Disconnect db
    self.container.close_database()

    #Reconnect to db
    try:
      db_file = self.container.loginFrame.db_file
      password = self.pre_pass_entry.get()
      self.container.db =Mydb(db_file, password)
      self.container.title( 'HaoPass: {}'.format(os.path.basename(db_file)) )

    except Exception as e:
      m = "Unable to connect. Please ensure current password is correct and try again."
      showerror(title='Error', message=m)
      return

    #Change Password
    try:
      self.container.db.changePassword(new_pass_1)
      m = "Your database password has been changed. Please remember it for future access."
      showinfo(title="Information", message=m)

      #Reset to empty
      self.pre_pass_entry.delete(0, tk.END)
      self.new_pass_1_entry.delete(0, tk.END)
      self.new_pass_2_entry.delete(0, tk.END)
      self.destroy()

    except Exception as e:
      showerror(title='Error', message=e)
      return

  #-----------------------
  #Bind to the close event 
  #-----------------------
  def on_close(self):

    #If not database, go to loginFrame
    if self.container.db is None:
      self.container.raise_loginFrame()

    #Destroy top
    self.destroy()
