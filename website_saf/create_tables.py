import sqlite3 as sql3

import pandas as pd 
non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename)
cursor = con.cursor()
# con.execute("DROP TABLE transactions")
# con.execute("CREATE TABLE transactions (email TEXT,type TEXT, Amount INTEGER, invest_date DATETIME,maturity_date DATETIME)")
# con.execute("DROP TABLE users")
# con.execute("CREATE TABLE users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL,referal_code TEXT)")
# con.execute("DROP TABLE fund_transactions")
# con.execute("CREATE TABLE fund_transactions (email TEXT,type TEXT, Amount INTEGER, fund_date DATETIME,wallet INT)")
# con.execute("DROP TABLE referral")
# con.execute("CREATE TABLE referral (email TEXT,refferal_code TEXT,refered_by TEXT,amount_refer_earned INT)")
# con.execute("DROP TABLE wallet")
# con.execute("CREATE TABLE wallet (email TEXT,wallet_ammount INTEGER);")


sql_statement = "select * from users;"
df = pd.read_sql_query(sql_statement, con)
print(df)
con.commit()
con.close()

