import sqlite3 as sql3
from flask import Flask,render_template,request,redirect,url_for,flash,session

non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
cursor = con.cursor()



def create_user(data):
    con.execute('INSERT INTO users VALUES (?,?,?)', data)
    con.commit()
    #pass

def login_user():
    con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
    cursor = con.cursor()
    query = """SELECT * from users"""
    cursor.execute(query)
    login_user.records = cursor.fetchall()
    
    
    #connection.execute('INSERT INTO StudentExamScores VALUES (?,?,?,?)', data)
    #pass
def insert_transactions(t_data):
    con.execute('INSERT INTO transactions VALUES (?,?,?,?,?)', t_data)
    con.commit()

def retrieve_transactions(email):
    con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
    cursor = con.cursor()
    cursor.execute('SELECT * from transactions WHERE email = ?',(email,))
    #('SELECT COUNT(Name) FROM "{}" WHERE Name=?'.format(group.replace('"', '""')), (food,))
    retrieve_transactions.records = cursor.fetchall()