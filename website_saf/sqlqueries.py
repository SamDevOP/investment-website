import sqlite3 as sql3
from flask import Flask,render_template,request,redirect,url_for,flash,session

from random import randint


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

def update_wallet(data):
    #UPDATE transactions SET wallet = ? WHERE email = ?
    con.execute('UPDATE fund_transactions SET wallet = ? WHERE email = ?',(data))
    con.commit()

def insert_funds(fund_data):
    con.execute('INSERT INTO fund_transactions VALUES (?,?,?,?,?)', fund_data)
    con.commit()

def fund_transactions(email):
    cursor.execute('SELECT * from fund_transactions WHERE email = ?',(email,))
    #('SELECT COUNT(Name) FROM "{}" WHERE Name=?'.format(group.replace('"', '""')), (food,))
    fund_transactions.records = cursor.fetchall()

def insert_referals(refer_data):
    con.execute('INSERT INTO referral VALUES (?,?,?)', refer_data)
    con.commit()

def get_referal(email,code,refered_by,amount_earned):
    cursor.execute('SELECT * from referral')
    refers=cursor.fetchall()
    #email,referal_code,refered_by,amount_earned
    # if refers==[]:
    #     insert_referals(())
    #for all in refers:






def generate_refer_code():
    
    code=randint(10000,99000)
    #if code in code_list:
    # for all in get_referal.records:
    #     if 

generate_refer_code()

