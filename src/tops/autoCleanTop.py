import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING

#=============================
#Top level Class: AutoCleanTop
#=============================
class AutoCleanTop(tk.Toplevel):

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
    self.var       = tk.StringVar()

  #---------------------
  #Init the info for top
  #---------------------
  def __init_top_info(self):

    w, h = 280, 250
    x, y = self.container.winfo_x(), self.container.winfo_y()
    self.geometry( "%dx%d+%d+%d" %(w,h,x+50,y+50) )
    self.title('Auto Clear Screen')

  #------------------
  #Create all widgets
  #------------------
  def __create_widgets(self):

    #Set var to auto_clear_screen
    default_value = "{:.1f}".format(self.container.viewFrame.auto_clear_screen)
    self.var.set(default_value) 

    #Create label and radiobuttons
    oneLabel = tk.Label(self, text="Screen will be cleared in:")
    oneLabel.grid(row = 0, column = 0, padx=10, pady=(10,5), sticky='NSW') 

    radio1 = tk.Radiobutton(self, text="30 Second", variable=self.var, value="0.5", command=self.selection)
    radio1.grid(row = 1, column = 0, padx=50, pady=5, sticky='NSW') 
    
    radio2 = tk.Radiobutton(self, text="1 minute", variable=self.var, value="1.0", command=self.selection)
    radio2.grid(row = 2, column = 0, padx=50, pady=5, sticky='NSW') 
    
    radio3 = tk.Radiobutton(self, text="2 minutes", variable=self.var, value="2.0", command=self.selection)
    radio3.grid(row = 3, column = 0, padx=50, pady=5, sticky='NSW') 

    radio3 = tk.Radiobutton(self, text="5 minutes", variable=self.var, value="5.0", command=self.selection)
    radio3.grid(row = 4, column = 0, padx=50, pady=5, sticky='NSW') 

    radio3 = tk.Radiobutton(self, text="15 minutes", variable=self.var, value="15.0", command=self.selection)
    radio3.grid(row = 5, column = 0, padx=50, pady=5, sticky='NSW') 

    radio3 = tk.Radiobutton(self, text="Never", variable=self.var, value="-1.0", command=self.selection)
    radio3.grid(row = 6, column = 0, padx=50, pady=5, sticky='NSW') 

  #---------------
  #After selection
  #---------------
  def selection(self):

    #Set auto_clear_screen
    v = float(self.var.get())
    self.container.viewFrame.auto_clear_screen = v
    self.container.viewFrame.reset_timer()