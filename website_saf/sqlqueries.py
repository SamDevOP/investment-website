import sqlite3 as sql3
from flask import Flask,render_template,request,redirect,url_for,flash,session

non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
cursor = con.cursor()



def create_user(data):
    con.execute('INSERT INTO users VALUES (?,?,?)', data)
    con.commit()
    #pass

def login_user(phonenum,passcode):
    con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
    cursor = con.cursor()
    records = cursor.fetchall()
    for each in records:
        if phonenum==each[2] and passcode==each[3]:
            print(passcode,phonenum)
            return redirect('/dashboard')
        else:
            flash("Number or Password not correct!")
    #connection.execute('INSERT INTO StudentExamScores VALUES (?,?,?,?)', data)
    #pass

def retrieve_transactions():
    pass