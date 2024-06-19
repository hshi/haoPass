import tkinter as tk
from tkinter import ttk, font
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.messagebox import askokcancel, WARNING

#==============================
#Top level Class: WelcomeAppTop
#==============================
class WelcomeAppTop(tk.Toplevel):

  #-------
  #Initial
  #-------
  def __init__(self, container, *args, **kwargs):

    #Initial
    super().__init__(container, *args, **kwargs)

    #Init variables
    self.container = container

    #Init the info for top
    self.__init_top_info()

    #Create widgets
    self.__create_widgets()

  #---------------------
  #Init the info for top
  #---------------------
  def __init_top_info(self):

    w, h = 400, 135
    x, y = self.container.winfo_x(), self.container.winfo_y()
    self.geometry( "%dx%d+%d+%d" %(w,h,x+50,y+50) )
    self.title('Welcome to HaoPass')

  #------------------
  #Create all widgets
  #------------------
  def __create_widgets(self):

    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)

    #Init info label
    info_label = tk.Text(self, bg='#f0f0f0')
    info_label.config(borderwidth=0, highlightthickness=0)
    info_label.tag_configure("center", justify="center")
    info_label.tag_configure("blue", foreground="blue")

    # Retrieve the default font used by the Text widget
    default_font = font.nametofont(info_label.cget("font"))
    bold_font = default_font.copy()
    bold_font.configure(weight="bold")
    info_label.tag_configure("bold", font=bold_font)

    info_label.grid(row = 0, column = 0, padx = 5, pady = (10,5), sticky='NESW')

    #Inset text
    label_text  = "Welcome to HaoPass Software\n\n"
    label_text += "This software helps you store strong, unique passwords for various online accounts." 
    label_text += "All the account information is securely encrypted.\n\n"
    label_text += "Developer: Hao Shi\n"
    label_text += "Email: masspebble@gmail.com\n"
    label_text += "All rights reserved.\n"
    info_label.insert(tk.END, label_text)
    info_label.tag_add("center", "1.0", "end")

    # Apply tags to specific text segments        
    start_index = label_text.index("Hao Shi")
    end_index = start_index + len("Hao Shi")
    info_label.tag_add("bold", f"1.0 + {start_index} chars", f"1.0 + {end_index} chars")

    start_index = label_text.index("masspebble@gmail.com")
    end_index = start_index + len("masspebble@gmail.com")
    info_label.tag_add("blue", f"1.0 + {start_index} chars", f"1.0 + {end_index} chars")

    info_label.config(state="disabled")