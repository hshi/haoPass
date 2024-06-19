import os

#============================
#Get the norm path of path_in
#============================
def normpath(path_in):

  if path_in is None or path_in == "":

    return path_in

  else:

    return os.path.normpath(path_in)