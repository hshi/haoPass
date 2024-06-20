import os
import sys

#============================
#Get the norm path of path_in
#============================
def normpath(path_in):

  if path_in is None or path_in == "":

    return path_in

  else:

    return os.path.normpath(path_in)

#========================
#Get Path for PyInstaller
#========================
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)