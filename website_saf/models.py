from apps import app
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app)
class User(db.Model):

    __tablename__ = 'Investors'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    phone = db.Column(db.String())
    passcode = db.Column(db.String())
    referal_code = db.Column(db.String())

    def __init__(self, email, phone, passcode,referal_code):
        self.email = email
        self.phone = phone
        self.passcode = passcode
        self.referal_code =referal_code


class Wallet(db.Model):
    __tablename__ = 'wallet'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    wallet_ammount = db.Column(db.String())
    
    def __init__(self, email, wallet_ammount):
        self.email = email
        self.wallet_ammount = wallet_ammount


class Referals(db.Model):
    __tablename__ = 'referals'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    refferal_code  = db.Column(db.String())
    refered_by = db.Column(db.String())
    amount_refer_earned = db.Column(db.String())

    def __init__(self, email, refferal_code , refered_by,amount_refer_earned):
        self.email = email
        self.refferal_code  = refferal_code 
        self.refered_by = refered_by
        self.amount_refer_earned =amount_refer_earned


class Investing(db.Model):
    __tablename__ = 'investing'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    amount = db.Column(db.Integer)
    maturity_date= db.Column(db.String())
    investment_date= db.Column(db.String())
    status = db.Column(db.String())
    date = db.Column(db.String())
    added_wallet = db.Column(db.String())
    invest_id = db.Column(db.String())

    def __init__(self, email,amount,maturity_date,investment_date,status,date,added_wallet,invest_id):
        self.email = email
        self.amount=amount
        self.maturity_date=maturity_date
        self.investment_date=investment_date
        self.status=status
        self.date =date 
        self.added_wallet=added_wallet
        self.invest_id=invest_id
        

class Activate(db.Model):
    __tablename__ = 'activate'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    status = db.Column(db.String())
    date = db.Column(db.String())

    def __init__(self, email, username, status,date):
        self.email = email
        self.username = username
        self.status = status
        self.date =date


#email TEXT,amount TEXT,request_id TEXT,status TEXT,date DATETIME
class Mpesax(db.Model):
    __tablename__ = 'mpesa'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    amount = db.Column(db.String())
    status = db.Column(db.String())
    date = db.Column(db.String())
    CheckoutRequestID=db.Column(db.String())

    def __init__(self, email, amount, status,date,CheckoutRequestID):
        self.email = email
        self.amount = amount
        self.status = status
        self.date =date
        self.CheckoutRequestID=CheckoutRequestID

#db.create_all()
