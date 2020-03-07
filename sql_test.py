import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		
	except Error as e:
		print(e)
	
	return conn



def create_user(conn, user):

	sql = ''' INSERT INTO users(discord,faceit)
			VALUES(?,?) '''
	cur = conn.cursor()
	cur.execute(sql, user)
	return cur.lastrowid

def delete_all_tasks(conn):

	sql = 'DELETE FROM users'
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
#returns the discord id from the faceit username
def get_discord(conn, faceit):
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE faceit=?", (faceit,))
	result = cur.fetchone()

	return result[0]
	









