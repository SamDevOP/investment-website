import sqlite3 as sql3
from flask import Flask,render_template,request,redirect,url_for,flash,session

from random import randint


non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
cursor = con.cursor()



def create_user(data):
    con.execute('INSERT INTO users VALUES (?,?,?,?)', data)
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



#REFERRAL CODE OPERATIONS

def generate_refer_code(mail,phone):
    mail_code=mail.split('@')
    refer_code=mail_code[0].upper()+str(phone[4:])
    return refer_code
##get referal code from users table
def retrieve_referal_code(email):
    cursor.execute('SELECT referal_code from users WHERE email = ?',(email,))
    return cursor.fetchone()[0]

#WALLET
def insert_wallet(w_data):
    con.execute('CREATE TABLE IF NOT EXISTS wallet(email TEXT PRIMARY KEY,wallet_ammount INT);')
    con.execute('INSERT INTO wallet VALUES (?,?)', w_data)
    con.commit()
    

def retrieve_wallet(email):
    cursor.execute('SELECT wallet_ammount from wallet WHERE email = ?',(email,))
    return cursor.fetchone()

def update_wallet(wt_data):
    con.execute('UPDATE wallet SET wallet_ammount  = ? WHERE email = ?',wt_data)
    con.commit()

## EARNING FROM REFERALS

def insert_referals_earned(er_data):
    con.execute('CREATE TABLE IF NOT EXISTS referrals(email TEXT,refferal_code TEXT,refered_by TEXT,amount_refer_earned INTEGER);')
    con.execute('INSERT INTO referrals VALUES (?,?,?,?)', er_data)
    con.commit()


def retrieve_referals(email):
    cursor.execute('SELECT * from referrals WHERE email = ?',(email,))
    return cursor.fetchall()

def retrieve_referals_numbers(code):
    cursor.execute('SELECT * from referrals WHERE refered_by = ?',(code,))
    return cursor.fetchall()

def retrieve_user_refcode():
    cursor.execute('SELECT referal_code from users;')
    return cursor.fetchall()

def retrieve_user_email(code):
    cursor.execute('SELECT email from users WHERE referal_code= ?;',(code,))
    return cursor.fetchone()


#INVESTING

def insert_investing(i_data):
    con.execute('CREATE TABLE IF NOT EXISTS investing(email TEXT,amount INTEGER,maturity_date DATETIME,investment_date DATETIME,status TEXT,date DATETIME,added_wallet TEXT,inv_id TEXT);')
    con.execute('INSERT INTO investing VALUES (?,?,?,?,?,?,?,?)', i_data)
    con.commit()

def retrieve_investing(email):
    con.execute('CREATE TABLE IF NOT EXISTS investing(email TEXT,amount INTEGER,maturity_date DATETIME,investment_date DATETIME,status TEXT,date DATETIME,added_wallet TEXT,inv_id TEXT);')
    cursor.execute('SELECT * from investing WHERE email = ?;',(email,))
    return cursor.fetchall()
    

def update_investing(ui_data):
    #con.execute('CREATE TABLE IF NOT EXISTS investing(email TEXT,amount INTEGER,maturity_date DATETIME,investment_date DATETIME,status TEXT,date DATETIME,added_wallet TEXT,inv_id TEXT);')
    con.execute('UPDATE investing SET status  = ? WHERE email = ? and inv_id=?',ui_data)
    con.commit()

def update_investing_added_wallet(ui_data):
    #con.execute('CREATE TABLE IF NOT EXISTS investing(email TEXT,amount INTEGER,maturity_date DATETIME,investment_date DATETIME,status TEXT,date DATETIME,added_wallet TEXT,inv_id TEXT);')
    con.execute('UPDATE investing SET added_wallet  = ? WHERE email = ?',ui_data)
    con.commit()


#returns number of investments a day
def select_number_of_inv(date):
    con.execute('CREATE TABLE IF NOT EXISTS investing(email TEXT,amount INTEGER,maturity_date DATETIME,investment_date DATETIME,status TEXT,date DATETIME,added_wallet TEXT);')
    cursor.execute('SELECT * from investing WHERE status = ? AND date = ?;',date)
    return cursor.fetchall()

# from datetime import datetime
# date=datetime.now().strftime("%d/%m/%Y")
# print(select_number_of_inv(("Live",str(date))))

