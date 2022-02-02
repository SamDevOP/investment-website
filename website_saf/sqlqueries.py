import sqlite3 as sql3
from random import randint

#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
non_normalized_db_filename='peakinvestors'
#non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename,check_same_thread=False)
cursor = con.cursor()

def create_user(data):
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    con.execute('INSERT INTO users VALUES (?,?,?,?)', data)
    con.commit()
    #pass

def login_user():
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    query = """SELECT * from users"""
    cursor.execute(query)
    login_user.records = cursor.fetchall()

def retrieve_username():
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    user_name=[]
    cursor.execute("SELECT referal_code from users")
    for i in cursor.fetchall():
        user_name.append(i[0])
    return user_name

def retrieve_user_phone(email):#sam@gmail.com
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    cursor.execute("SELECT phone from users WHERE email=?",(email,))
    phone=cursor.fetchone()[0]
    return phone


def retrieve_password(email):
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    cursor.execute("SELECT passcode from users WHERE email=?",(email,))
    return cursor.fetchone()[0]



"""=============================Users============================================="""



    
    
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
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    cursor.execute('SELECT referal_code from users WHERE email = ?',(email,))
    return cursor.fetchone()[0]

#WALLET
def insert_wallet(w_data):
    con.execute('CREATE TABLE IF NOT EXISTS wallet(email TEXT PRIMARY KEY,wallet_ammount INT);')
    con.execute('INSERT INTO wallet VALUES (?,?)', w_data)
    con.commit()
    

def retrieve_wallet(email):
    con.execute('CREATE TABLE IF NOT EXISTS wallet(email TEXT PRIMARY KEY,wallet_ammount INT);')
    cursor.execute('SELECT wallet_ammount from wallet WHERE email = ?',(email,))
    return cursor.fetchone()[0]

def update_wallet(wt_data):
    con.execute('UPDATE wallet SET wallet_ammount  = ? WHERE email = ?',wt_data)
    con.commit()

## EARNING FROM REFERALS

def insert_referals_earned(er_data):
    con.execute('CREATE TABLE IF NOT EXISTS referrals(email TEXT,refferal_code TEXT,refered_by TEXT,amount_refer_earned INTEGER);')
    con.execute('INSERT INTO referrals VALUES (?,?,?,?)', er_data)
    con.commit()


def retrieve_referals(email):
    con.execute('CREATE TABLE IF NOT EXISTS referrals(email TEXT,refferal_code TEXT,refered_by TEXT,amount_refer_earned INTEGER);')
    cursor.execute('SELECT * from referrals WHERE email = ?',(email,))
    return cursor.fetchall()

def retrieve_referals_numbers(code):
    con.execute('CREATE TABLE IF NOT EXISTS referrals(email TEXT,refferal_code TEXT,refered_by TEXT,amount_refer_earned INTEGER);')
    cursor.execute('SELECT * from referrals WHERE refered_by = ?',(code,))
    return cursor.fetchall()

def retrieve_user_refcode():
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
    cursor.execute('SELECT referal_code from users;')
    return cursor.fetchall()

def retrieve_user_email(code):
    con.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT);')
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




#ACTIVATING ACCOUNT
def insert_activate(i_data):
    con.execute('CREATE TABLE IF NOT EXISTS activate(email TEXT,username TEXT,status TEXT);')
    con.execute('INSERT INTO activate VALUES (?,?,?)', i_data)
    con.commit()


def retrieve_activate(email):
    con.execute('CREATE TABLE IF NOT EXISTS activate(email TEXT,username TEXT,status TEXT);')
    cursor.execute('SELECT status from activate WHERE email = ?;',(email,))
    return cursor.fetchone()
    

def update_activate(ui_data):
    con.execute('CREATE TABLE IF NOT EXISTS activate(email TEXT,username TEXT,status TEXT);')
    con.execute('UPDATE activate SET status  = ? WHERE email = ?',ui_data)
    con.commit()

#MPEPE
def insert_mpesa(i_data):
    con.execute('CREATE TABLE IF NOT EXISTS mpesa(email TEXT,amount TEXT,request_id TEXT,status TEXT,date DATETIME);')
    con.execute('INSERT INTO mpesa VALUES (?,?,?,?)', i_data)
    con.commit()

def retrieve_mpesa(request_id):
    con.execute('CREATE TABLE IF NOT EXISTS mpesa(email TEXT,amount TEXT,request_id TEXT,status TEXT,date DATETIME);')
    cursor.execute('SELECT status from mpesa WHERE request_id = ?;',(request_id,))
    return cursor.fetchone()




# from datetime import datetime
# date=datetime.now().strftime("%d/%m/%Y")
# print(select_number_of_inv(("Live",str(date))))
#print(retrieve_user_phone(email))

#print(retrieve_wallet("samwel@gmail.com")[0])



#update_activate(("ACTIVATED","sam@gmail.com"))

