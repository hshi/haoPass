import os
import ast
from sqlcipher3 import dbapi2 as sqlite
from sqlcipher3.dbapi2 import Error

#===========================
#Escape string for format(s)
#===========================
def escape_str(s):

	#Escape backslashes first
	s = s.replace("\\", "\\\\")

	#Escape single quote
	s = s.replace("'", "\\'")

	#For """PRAGMA key = "{}";""", we can not have " in key
	s = s.replace('"', "\\'")
	
	return s

#==========
#Mydb Class
#==========
class Mydb():

	#------------------------------------
	#Constructor: connect to the database
	#------------------------------------
	def __init__(self, db_file, password):

		#Init self.conn
		self.conn = None

		#Login to password
		self.__login(db_file, password)

	#---------------------
	#Login to the database
	#---------------------
	def __login(self, db_file, password):

		try:
			self.conn = sqlite.connect(db_file)

			escape_pass = escape_str(password)
			self.commit_command("""PRAGMA key = "{}";""".format(escape_pass))
			self.commit_command("""PRAGMA cipher_compatibility = 3;""")
			self.commit_command("""PRAGMA foreign_keys=ON;""")

			#Try a simple query to verify the password
			data = self.query_data("SELECT count(*) FROM sqlite_master")	

		except Error as e:
			raise Exception(e)

	#-------------------------------
	#Change password of the database
	#-------------------------------
	def changePassword(self, password):

		try:
			#rekey
			escape_pass = escape_str(password)
			self.commit_command("""PRAGMA rekey = "{}";""".format(escape_pass))

			#Try a simple query to verify the password
			data = self.query_data("SELECT count(*) FROM sqlite_master")	

		except Error as e:
			raise Exception(e)

	#--------------------------------------
	#Destructor: disconnect to the database
	#--------------------------------------
	def __del__(self):

		self.disconnect()

	#--------------------------
	#Disconnect to the database
	#--------------------------
	def disconnect(self):
		
		if self.conn:
			self.conn.close()

	#--------------
	#Create a table
	#--------------
	def create_table(self, command_sql):

		try:
			cur = self.conn.cursor()
			cur.execute(command_sql)
		except Error as e:
			raise Exception(e)

	#----------------------------------------
	#Commit a command an return the lastrowid
	#----------------------------------------
	def commit_command(self, command_sql, data=None):

		try:
			cur = self.conn.cursor()
			if data is None: cur.execute(command_sql)
			else: cur.execute(command_sql, data)
			self.conn.commit()
			return cur.lastrowid
		except Error as e:
			raise Exception(e)

	#----------------------
	#Query data from sqlite
	#----------------------
	def query_data(self, command_sql, data=None):

		try:
			cur = self.conn.cursor()
			if data is None: cur.execute(command_sql)
			else: cur.execute(command_sql, data)
			rows = cur.fetchall()
			return rows
		except Error as e:
			raise Exception(e)

	#-------------------------------
	#Write one account into database
	#-------------------------------
	def write_one_account(self, entry):

		#Get Required
		account  = entry['Account']
		username = entry['Username']
		password = entry['Password']

		#Get Optional
		exclude_keys = ["Account", "Username", "Password"]
		other_entry  = {key: value for key, value in entry.items() if key not in exclude_keys}
		others = str(other_entry)

		#Insert user table
		sql_insert_table = """
				INSERT INTO accounts (account, username, password, others) 
				VALUES (?, ?, ?, ?)
		"""
		row_id = self.commit_command(sql_insert_table, (account, username, password, others) ) 

		return "New account (ID {}) has been submitted for secure storage.".format(row_id)

	#------------------------------
	#Update one account in database
	#------------------------------
	def update_one_account(self, entry, account_id):

		#Get Required
		account  = entry['Account']
		username = entry['Username']
		password = entry['Password']

		#Get Optional
		exclude_keys = ["Account", "Username", "Password"]
		other_entry  = {key: value for key, value in entry.items() if key not in exclude_keys}
		others = str(other_entry)

		#Insert user table
		sql_insert_table = """
													UPDATE accounts 
													set account=?, username=?, password=?, others=?
													WHERE account_id=?
											 """
		self.commit_command(sql_insert_table, (account, username, password, others, account_id) ) 

		return "Account (ID {}) has been updated.".format(account_id)

	#-------------------------
	#Read accounts with filter
	#-------------------------
	def read_account_filter(self, 
													row_count, 
													offset, 
													account="", 
													username="", 
													password="", 
													others=""):

		#Filter data from database
		sql_query_data = """
												SELECT account_id, account, username, password, others
												FROM accounts
												WHERE account  LIKE ?
													AND username LIKE ?
													AND password LIKE ?
													AND others   LIKE ?
												ORDER BY account_id DESC
												LIMIT ? OFFSET ?;
										 """
		filter_words = ('%'+account+'%', '%'+username+'%', '%'+password+'%', '%'+others+'%', row_count, offset)
		data = self.query_data(sql_query_data, filter_words)

		#Transfer data to dict
		len_accounts = len(data); accounts=[]
		for i in range(len_accounts):
			entry = {}
			entry["ID"]       = data[i][0]
			entry["Account"]  = data[i][1]
			entry["Username"] = data[i][2]
			entry["Password"] = data[i][3]
			entry.update( ast.literal_eval(data[i][4]) )
			accounts.append(entry)

		return accounts

	#------------------------------
	#Get the matched account number
	#------------------------------
	def read_account_num_filter(self, 
															account="", 
															username="", 
															password="", 
															others=""):

		#Filter data from database
		sql_query_data = """
												SELECT COUNT(account_id) AS total_rows
												FROM accounts
												WHERE account  LIKE ?
													AND username LIKE ?
													AND password LIKE ?
													AND others   LIKE ?
												ORDER BY account_id DESC;
										 """
		filter_words = ('%'+account+'%', '%'+username+'%', '%'+password+'%', '%'+others+'%')
		data = self.query_data(sql_query_data, filter_words)

		return data[0][0]

	#-------------------------------
	#Delete on account by account id
	#-------------------------------
	def delete_one_account(self, account_id):

		sql_delete_table = """ DELETE FROM accounts
													 WHERE account_id=?;
											 """

		row_id = self.commit_command(sql_delete_table, (account_id,))

		return "Account (ID {}) has been deleted.".format(account_id)

#=====================
#Create data base file
#=====================
def createMyDataBase(dataFile, password):

	#Remove dataFile and create db
	if os.path.exists(dataFile):
		os.remove(dataFile)
	db = Mydb(dataFile, password)

	#Create accounts table
	sql_create_table = """ CREATE TABLE IF NOT EXISTS accounts (
													 account_id integer PRIMARY KEY,
													 account text NOT NULL,
													 username text NOT NULL,
													 password text NOT NULL,
													 others text
														 ); """
	db.create_table(sql_create_table)

	return db

#=========
#Main Code
#=========
if __name__ == "__main__":

	# createMyDataBase("../data.db", "245")

	mydb = Mydb("../data.db", "245")
	sql_query_data = """ SELECT account_id, account, username, password, others
											 FROM accounts
											 ORDER BY account_id; 
									 """
	data = mydb.query_data(sql_query_data)
	print(data)