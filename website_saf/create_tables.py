import sqlite3 as sql3

import pandas as pd 
non_normalized_db_filename='spin_pesa'

con = sql3.connect(non_normalized_db_filename)
cursor = con.cursor()
#con.execute("CREATE TABLE transactions (phone TEXT PRIMARY KEY, Amount INTEGER, time DATETIME)")
#con.execute("CREATE TABLE users (email TEXT PRIMARY KEY,phone TEXT,passcode VARCHAR NOT NULL)")
#con.execute("SELECT * FROM users")

sql_statement = "select * from users;"
df = pd.read_sql_query(sql_statement, con)
print(df)
con.commit()
con.close()

