import app
class User(app.db.Model):
    __tablename__ = 'user'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    phone = app.db.Column(app.db.String())
    passcode = app.db.Column(app.db.String())
    referal_code = app.db.Column(app.db.String())

    def __init__(self, email, phone, passcode,referal_code):
        self.email = email
        self.phone = phone
        self.passcode = passcode
        self.referal_code =referal_code


    # def __repr__(self):
    #     return '<id {}>'.format(self.id)
    
    # def serialize(self):
    #     return {
    #         'id': self.id, 
    #         'email': self.email,
    #         'phone': self. phone,
    #         'passcode':self.passcode,
    #         'referal_code':self.referal_code
    #     }


class Wallet(app.db.Model):
    __tablename__ = 'wallet'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    wallet_ammount = app.db.Column(app.db.String())
    
    def __init__(self, email, wallet_ammount):
        self.email = email
        self.wallet_ammount = wallet_ammount


class Referals(app.db.Model):
    __tablename__ = 'referals'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    refferal_code  = app.db.Column(app.db.String())
    refered_by = app.db.Column(app.db.String())
    amount_refer_earned = app.db.Column(app.db.String())

    def __init__(self, email, refferal_code , refered_by,amount_refer_earned):
        self.email = email
        self.refferal_code  = refferal_code 
        self.refered_by = refered_by
        self.amount_refer_earned =amount_refer_earned


class Investing(app.db.Model):
    __tablename__ = 'investing'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    amount = app.db.Column(app.db.Integer)
    maturity_date= app.db.Column(app.db.String())
    investment_date= app.db.Column(app.db.String())
    status = app.db.Column(app.db.String())
    date = app.db.Column(app.db.String())
    added_wallet = app.db.Column(app.db.String())
    invest_id = app.db.Column(app.db.String())

    def __init__(self, email,amount,maturity_date,investment_date,status,date,added_wallet,invest_id):
        self.email = email
        self.amount=amount
        self.maturity_date=maturity_date
        self.investment_date=investment_date
        self.status=status
        self.date =date 
        self.added_wallet=added_wallet
        self.invest_id=invest_id
        

class Activate(app.db.Model):
    __tablename__ = 'activate'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    username = app.db.Column(app.db.String())
    status = app.db.Column(app.db.String())
    date = app.db.Column(app.db.String())

    def __init__(self, email, username, status,date):
        self.email = email
        self.username = username
        self.status = status
        self.date =date


#email TEXT,amount TEXT,request_id TEXT,status TEXT,date DATETIME
class Mpesax(app.db.Model):
    __tablename__ = 'mpesa'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String())
    amount = app.db.Column(app.db.String())
    status = app.db.Column(app.db.String())
    date = app.db.Column(app.db.String())
    CheckoutRequestID=app.db.Column(app.db.String())

    

    def __init__(self, email, amount, status,date,CheckoutRequestID):
        self.email = email
        self.amount = amount
        self.status = status
        self.date =date
        self.CheckoutRequestID=CheckoutRequestID


