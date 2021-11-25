import sqlite3 as sql3

non_normalized_db_filename='spin_pesa'

connection = sql3.connect(non_normalized_db_filename)
cursor = connection.cursor()

def create_user(data):
    #connection.execute('INSERT INTO StudentExamScores VALUES (?,?,?,?)', data)
    pass

def login_user(data):
    #connection.execute('INSERT INTO StudentExamScores VALUES (?,?,?,?)', data)
    pass

def retrieve_transactions():
    pass