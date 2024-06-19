import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from src.auxiliary.useful import normpath

#===============
#MyDefault Class
#===============
class MyDefault():

	#-------
	#Initial
	#-------
	def __init__(self):

		#Set filename
		self.filename = os.getcwd() + "\\default.txt"

		#Set isUpdate
		self.isUpdate = False

		#load self.data
		self.load()

	#-------------
	#Load the data
	#-------------  
	def load(self):

		#Get default
		if os.path.isfile(self.filename):

			#If file exist, load it.
			with open(self.filename, 'r') as openfile:
				self.data = json.load(openfile)

		else:

			#Create default and save to file
			self.create()

	#---------------
	#Create the data
	#---------------  
	def create(self):

		self.data = {}
		self.data["winfo_width"]  = 580
		self.data["winfo_height"] = 520
		self.data["default_winfo_width"]  = 580
		self.data["default_winfo_height"] = 520
		self.data["auto_clean_min"] = 5.0
		self.data["auto_logout_min"] = 15.0
		self.data["database_file"] = ""

		with open(self.filename, "w") as data_file:
			data = json.dumps(self.data, indent=4)
			data_file.write(data)

	#-------------
	#Save the data
	#-------------
	def save(self):

		if self.isUpdate:  
			with open(self.filename, "w") as data_file:
				data = json.dumps(self.data, indent=4)
				data_file.write(data)

	#------------
	#Get win_size
	#------------
	def get_win_size(self):

		return self.data['winfo_width'], self.data['winfo_height']

	#--------------------
	#Get default win_size
	#--------------------
	def get_default_win_size(self):

		return self.data['default_winfo_width'], self.data['default_winfo_height']

	#------------------
	#Get auto_clean_min
	#------------------
	def get_auto_clean(self):

		return self.data['auto_clean_min']

	#-------------------
	#Get auto_logout_min
	#-------------------
	def get_auto_logout(self):

		return self.data['auto_logout_min']

	#-----------------
	#Get database_file
	#-----------------
	def get_db_file(self):

		return self.data['database_file']

	#---------------
	#Update win_size
	#---------------
	def update_win_size(self, winfo_width, winfo_height):

		if( self.data['winfo_width']  != winfo_width  or
				self.data['winfo_height'] != winfo_height   ):

			#Ask if update
			answer = askokcancel(title="Confirmation", 
													 message="Do you want to save current screen size as default?", 
													 icon=WARNING)

			#If Answer yes, update
			if answer:
				self.isUpdate = True
				self.data['winfo_width']  = winfo_width
				self.data['winfo_height'] = winfo_height

	#-----------------
	#Update auto_clean
	#-----------------
	def update_auto_clean(self, auto_clean_min):

		if self.data['auto_clean_min'] != auto_clean_min:

			#Ask if update
			answer = askokcancel(title="Confirmation", 
													 message="Do you want to save auto clean parameter {:.1f} as default?".format(auto_clean_min), 
													 icon=WARNING)

			#If Answer yes, update
			if answer:
				self.isUpdate = True
				self.data['auto_clean_min'] = auto_clean_min

	#------------------
	#Update auto_logout
	#------------------
	def update_auto_logout(self, auto_logout_min):

		if self.data['auto_logout_min'] != auto_logout_min:

			#Ask if update
			answer = askokcancel(title="Confirmation", 
													 message="Do you want to save auto logout parameter {:.1f} as default?".format(auto_logout_min), 
													 icon=WARNING)

			#If Answer yes, update
			if answer:
				self.isUpdate = True
				self.data['auto_logout_min'] = auto_logout_min

	#--------------------
	#Update database_file
	#--------------------
	def update_database_file(self, database_file):

		#Update database_file
		if( normpath(self.data['database_file']) != normpath(database_file) ):

			#Get business name
			database_name = "None"
			if database_file != "":
				database_name = os.path.basename(database_file)

			#Ask if update
			answer = askokcancel(title="Confirmation", 
													 message="Do you want to save current database {} as default?".format(database_name), 
													 icon=WARNING)

			#If Answer yes, update
			if answer:
				self.isUpdate = True
				self.data['database_file'] = database_file