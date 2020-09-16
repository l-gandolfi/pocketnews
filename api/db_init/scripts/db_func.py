'''
@title: CRUD functions for DB

Instruction:
sudo apt-get install sqlite3
sudo apt-get install sqlitebrowser
'''
import sqlite3
import json
import os.path as path
import numpy as np
import pandas as pd
import io

DB_PATH = path.abspath('./') + '/db_init/tweets_data/'

class Functions:

	def __init__(self, DB_PATH):
		super().__init__()
		(self.cur, self.con) = self.getConnection()
		# Converts np.array to TEXT when inserting
		sqlite3.register_adapter(np.ndarray, self.adapt_array)
		# Converts TEXT to np.array when selecting
		sqlite3.register_converter("array", self.convert_array)
		self.createDatabase()

	def getConnection(self):
		# Connection to database
		connection = sqlite3.connect(DB_PATH + 'full_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
		cursor = connection.cursor()
		return (cursor, connection)

	def createDatabase(self):
		# Create table
		self.cur.execute('CREATE TABLE IF NOT EXISTS Tweets(tweet_id INTEGER PRIMARY KEY AUTOINCREMENT, tweet TEXT, topic BLOB, vector array, date VARCHAR(32))')
		self.cur.execute('CREATE TABLE IF NOT EXISTS Users(user_id INTEGER, tweet_id INTEGER, topic topic VARCHAR(64), vector array)')
		#self.cur.execute("create table test (arr array)")

	def dropTables(self, tname):
		# Drop table
		self.cur.execute('DROP TABLE ' + tname)
		
	'''
	Funzione di appoggio per salvare un numpy array
	'''
	def adapt_array(self, arr):
		out = io.BytesIO()
		np.save(out, arr)
		out.seek(0)
		return sqlite3.Binary(out.read())
		
	'''
	Funzione di appoggio per convertire un numpy array nel tipo corretto
	'''
	def convert_array(self, text):
		out = io.BytesIO(text)
		out.seek(0)
		#print(out)
		return np.load(out)
    
	def readAllTweets(self):
		try:
			# Read all data in db
			self.cur.execute('SELECT * FROM Tweets')
			rows = self.cur.fetchall()
		except:
			print('Data read failed')

		return rows

	def readAllUsers(self):
		try:
			# Read all data in db
			self.cur.execute('SELECT * FROM Users')
			rows = self.cur.fetchall()
		except:
			print('Data read failed')

		return rows

	def readTweetsData(self, id):
		row = []
		try:
			# Read data by id
			self.cur.execute('SELECT * FROM Tweets WHERE tweet_id=?', (id, ))
			row = self.cur.fetchall()
		except:
			print('Data read failed')

		return row

	def readUsersData(self, id):
		row = []
		try:
			# Read data by id
			self.cur.execute('SELECT * FROM Users WHERE user_id=?', (id, ))
			row = self.cur.fetchall()
		except:
			print('Data read failed')

		return row
