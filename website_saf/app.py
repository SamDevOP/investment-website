#from werkzeug import secure_filename

from dataclasses import dataclass
from math import remainder
import re
from traceback import StackSummary
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
import os
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
#from sqlqueries import *
from mpesa_views import *
from datetime import datetime,timedelta
import base64
from flask_sqlalchemy import SQLAlchemy
from withdraw import *

#from db_config import *
from my_model import *



#Initializing flask app
app=Flask(__name__)

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1AHEKSpdsr465dgjgjhs78686siugdhsk9239'

ENV ="dev"

if ENV=="dev":
    app.debug==True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:samis100%code@localhost/peakinvestors'
    Base_URL="https://peakinvestors-app.herokuapp.com/"
else:
    app.debug==False
    Base_URL="https://peakinvestors.co.ke/"
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

def commit_data(data):
    db.session.add(data)
    db.session.commit()


def active():
    active_account=db.session.query(Activate).filter(Activate.email==session["email"]).first()
    if active_account.status=="DEACTIVATED":
        account_status=1
    else:
        account_status=2

    return account_status






@app.route('/',methods =["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        phonenum=request.form["email"]
        pass_code=request.form["password"]
        person=db.session.query(User).filter(User.email==phonenum).first()
        if person.passcode==pass_code:
            session["email"]=person.email
            #return redirect('/dashboard')
            return redirect('/referrals')

            #print(session["email"])
        else:
            flash("Email or Password not correct!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'email' in session:  
        session.pop('email',None)  
        return redirect("/login")  
    else:  
        return '<p>user already logged out</p>' 



@app.route('/signup',methods =["GET","POST"])
@app.route('/signup/<referral_code>',methods =["GET","POST"])
@app.route('/<referral_code>',methods =["GET","POST"])
def signup(referral_code=None):
    if referral_code:
        referral_c = referral_code
    else:
        referral_c = ''
    if request.method== "POST":
        mail=request.form["email"]
        phone=request.form["phone"]
        username = request.form["username"]       
            #add a fetch all to chech for emails and phone duplication
        root_pass=request.form["password"]
        repeat_pass=request.form["cpassword"]

        join_date=datetime.now().strftime("%d%m%Y")
            
        if root_pass != repeat_pass:
            flash('Passwords Do not match')
        else:
            if len(root_pass)<8:
                flash("Your Password should be more than 8 Characters")
            else:
                if db.session.query(User).filter(User.referal_code==username).count()!=0:
                    flash("Username exists. Choose another.")
                else:
                    #r_code=generate_refer_code(mail,phone)
                    if db.session.query(User).filter(User.email==mail).count()!=0:
                        flash("Account with that email already exists.")
                    else:
                        if len(phone)!=12:
                            flash("Mpesa phone number is incorrect. Format is: 2547XXXXXXXX")
                        else:
                            
                            if referral_c!='':    
                                if db.session.query(User).filter(User.referal_code==referral_c).count()>0:
                                    create_users=User(mail,phone,root_pass,username)
                                    commit_data(create_users)

                                    wallet = 0
                                    inserting_wallet=Wallet(mail,wallet)
                                    commit_data(inserting_wallet)
                                    

                                    inserting_activate=Activate(mail,username,"DEACTIVATED",join_date)
                                    commit_data(inserting_activate)

                                    insert_referals_earn=Referals(mail,username,referral_c,200)
                                    commit_data(insert_referals_earn)
                                    wallet_email=db.session.query(User).filter(User.referal_code==referral_c).first()
                                    r_wallet=db.session.query(Wallet).filter(Wallet.email==wallet_email.email).first()
                                    r_wallet.wallet_ammount=int(r_wallet.wallet_ammount) + 200
                                    db.session.commit()

                                    flash("Account created Successfully!") 
                                    return redirect("/login") 
                                else:
                                    flash("Your link is broken, copy it and try again")
                                    #add error page here
                            else:
                                create_users=User(mail,phone,root_pass,username)
                                commit_data(create_users)

                                wallet = 0
                                inserting_wallet=Wallet(mail,wallet)
                                commit_data(inserting_wallet)

                                inserting_activate=Activate(mail,username,"DEACTIVATED",join_date)
                                #inserting_activate=Activate("rectangularsolutions@protonmail.com","rectangle","DEACTIVATED",join_date)
                                commit_data(inserting_activate)
                            

                                flash("Account created Successfully!")
                                return redirect("/login")  
    return render_template('signup.html')


@app.route('/dashboard',methods =["GET","POST"])
def dashboard():
    #retrieve_transactions(session['email'])
    #fund_transactions(session['email'])
    if "email" not in session:
        return redirect(url_for('login')) 

    else:

        my_records= db.session.query(Investing).filter(Investing.email==session['email']).all()
       
        if db.session.query(Investing).filter(Investing.email==session['email']).count()==0:
            amount_invested= 0
            expected_income=  0
            #invest_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            maturitydate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            maturity_date= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            time_remaining=0.0
            remaining_time=0
        else:
            total_revenue=[]
            total_invested=[]
            remaining_time=[]
            today=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            today=datetime.now().strptime(today,'%d/%m/%Y %H:%M:%S')

            for all in my_records:
                maturity_date= datetime.strptime(all.maturity_date, '%d/%m/%Y %H:%M:%S')
                time_remaining = maturity_date - datetime.now()
                remaining_time.append(time_remaining.total_seconds())
                if time_remaining.total_seconds()>0:
                    all.status='Live'
                    db.session.commit()
                    
                else:  
                    all.status='Done'
                    db.session.commit()
                    

                    
            
            wallet = db.session.query(Wallet).filter(Wallet.email==session['email']).first()
            print(type(int(wallet.wallet_ammount)))
            my_records= db.session.query(Investing).filter(Investing.email==session['email']).all()
            for all in my_records:
                if all.status=="Live" and all.added_wallet=="NO":
                    total_invested.append(all.amount)
                    total_revenue.append((int(all.amount) + (int((int(all.amount)*0.4)))))

                elif all.status == "Done" and all.added_wallet=="NO":
                    wallet.wallet_ammount = int(wallet.wallet_ammount) + int(all.amount) + int((int(all.amount)*0.4))
                                        
                    all.added_wallet="YES"
                    db.session.commit()
                  
                else:
                    continue
                
                
            expected_income=sum(total_revenue)
            amount_invested=sum(total_invested)
    
        
        refered_by=db.session.query(User).filter(User.email==session['email']).first()
        total_referals=db.session.query(Referals).filter(Referals.refered_by==refered_by.referal_code).count()
        wallet =  wallet = db.session.query(Wallet).filter(Wallet.email==session['email']).first()


    return render_template('dashboard_home.html',my_records=my_records,expected_income=expected_income,\
        amount_invested=amount_invested,remaining_time=time_remaining,wallet=wallet.wallet_ammount,total_referals=total_referals,account_status=active())
    


@app.route('/referrals')
def refer():
    db=SQLAlchemy(app)

    if session['email']=="":
        return redirect("/login")
    else:
        mail=session['email']
        refer_=db.session.query(User).filter(User.email==mail).first()

        referral_link=Base_URL+refer_.referal_code
    
        return render_template('refer.html',referral_link=referral_link,account_status =active())


@app.route('/withdraw',methods =["GET","POST"])
def withdraw():
    if request.method == "POST":
        withdrawn_cash = int(request.form["withdraw_cash"])
        #the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        wallet=db.session.query(Wallet).filter(Wallet.email==session['email']).first()
        phone_num=db.session.query(User).filter(User.email==session['email']).first()
        status=db.session.query(Activate).filter(Activate.email==session['email']).first()
        print(os.environ.get("DATABASE_URL"))
        if status.status == "DEACTIVATED":
            flash("Activate account to be able to invest")
        else:
            if withdrawn_cash<=1000:
                transaction_cost=30
            elif withdrawn_cash>1000:
                transaction_cost=50

            withdraw_cash = withdrawn_cash + transaction_cost
            if withdraw_cash>=int(wallet.wallet_ammount):
                flash("Your transaction cannot be completed due to insufficient Funds")
            else:
                cash_out=B2C()
                cashOut=cash_out.transact(initiator_name=session["email"],amount="1",party_b=phone_num.phone)
                if cashOut["ResponseCode"] == "0":
                    mpepe=Mpesax(session['email'],withdrawn_cash,"WITHDRAWAL",datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"")
                    wallet.wallet_ammount = int(wallet.wallet_ammount) - withdraw_cash
                    db.session.commit()
                    flash("Withdrawn " + str(withdrawn_cash) + " Cost of Transaction: "+ str(transaction_cost) )
                else:
                    flash("Cannot complete transaction")
    return render_template('withdraw.html',account_status =active())  

@app.route('/fund',methods =["GET","POST"])
def fund():
    if request.method == "POST":

        fund_cash = request.form["fund_cash"]
        #the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #add Mpesa transaction information here
        phone_num=db.session.query(User).filter(User.email==session['email']).first()
        
        acc_status=db.session.query(Activate).filter(Activate.email==session['email']).first()
        lipa=MpesaExpress()
        if acc_status.status == "DEACTIVATED":
            flash("Activate account to be able to invest")
        else:
            stkpush=lipa.stk_push(amount=str(fund_cash),phone_number=phone_num.phone)
            if "ResponseCode" in stkpush:
                if stkpush["ResponseCode"] ==  "0":
                    time.sleep(2)
                    flash("Payment request has been sent to your number")
                    mpepe=Mpesax(session['email'],fund_cash, "0", date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), CheckoutRequestID=stkpush["CheckoutRequestID"])
                    commit_data(mpepe)
                    return redirect(url_for('confirm_funds',amount=fund_cash,request_id=stkpush["CheckoutRequestID"],status="0",**request.args))
                            #return redirect("/confirm_payment")
                else:
                    flash("Payment request failed. Try again later")
            else:
                flash("Payment request failed. Try again later")
            #insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
    return render_template('fund_acct.html',account_status =active())


@app.route('/confirm_funds/<request_id>/<amount>/<status>',methods =["GET","POST"])
def confirm_funds(amount=None,request_id=None,status=None):
    if amount and request_id and status:
        amount_sent=amount
        requested_id=request_id
        state=status
        print(amount_sent,requested_id,state)
    else:
        flash("Can not Confirm payment")
    if request.method =="POST":
        wallet=db.session.query(Wallet).filter(Wallet.email==session['email']).first()
        RequestID=db.session.query(Mpesax).filter(Mpesax.email==session['email'],Mpesax.CheckoutRequestID==requested_id,Mpesax.status==state,Mpesax.amount==amount_sent).first()
        lipa=MpesaExpress()
        check_stkpush=lipa.query(checkout_request_id=RequestID.CheckoutRequestID)
        #check_stkpush=lipa.query(checkout_request_id="ws_CO_010220221355142049")
        if check_stkpush["ResultCode"]== "0":
            wallet.wallet_ammount=int(wallet.wallet_ammount)+ int(amount_sent)
            RequestID.status="1"
            db.session.commit()

        else:
            RequestID.status=check_stkpush["ResultDesc"]
            db.session.commit()
            flash(check_stkpush["ResultDesc"]+"Try Again Later")

        
    return render_template("mpesa.html")

@app.route('/invest',methods =["GET","POST"])
def invest():
    if request.method == "POST":
        
        fund_cash = request.form["fund_cash"]
        investment_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date=datetime.now().strftime("%d%m%Y")
        maturity_date=(datetime.now() + timedelta(hours=72)).strftime("%d/%m/%Y %H:%M:%S") #(hours=72)
        the_date=str(datetime.now().strftime("%d%m%Y"))
        inv_id='INV0'

        if session['email'] == "":
            return redirect(url_for('login'))
        else:

            my_data = db.session.query(Investing).filter(Investing.email==session["email"]).count()

            wallet=db.session.query(Wallet).filter(Wallet.email==session["email"]).first()

            if db.session.query(Investing).filter(Investing.email==session["email"]).count()==0:
                inv_id=inv_id + str(my_data)
                if int(fund_cash)> int(wallet.wallet_ammount):
                    flash("You have insufficient balance to complete the investment")
                    return redirect('/fund')
                else:
                    inserting_invest=Investing(session['email'],fund_cash,maturity_date,investment_date,'Live',date,'NO',inv_id)
                    commit_data(inserting_invest)

                    
                    wallet.wallet_ammount=int(wallet.wallet_ammount)-int(fund_cash)
                    db.session.commit()                    
                    flash("You have invested " + str(fund_cash))
                    
            else:
                inv_id=inv_id + str(my_data)
                if db.session.query(Investing).filter(Investing.email==session["email"],Investing.date==the_date,Investing.status=="Live").count()<=2:
                    
                    if int(fund_cash)> int(wallet.wallet_ammount):
                        flash("You have insufficient balance to complete the investment")
                        return redirect('/fund')
                    else:
                        insert_invest=Investing(session['email'],fund_cash,maturity_date,investment_date,'Live',date,'NO',inv_id)
                        commit_data(insert_invest)

                        wallet.wallet_ammount=int(wallet.wallet_ammount)-int(fund_cash)
                        db.session.commit()

                        flash("You have invested " + str(fund_cash))
                else:
                    flash("You have exhausted your investment opportunities for today")
    return render_template('invest.html',account_status =active())    




"""============================================ACTIVATE ACCOUNT======================"""

@app.route('/activate',methods =["GET","POST"])
def activate():
    if request.method == "POST":
        #acc_status=acc_status=db.session.query(Activate).filter(Activate.email==session['email']).first()
        
        phone_num=db.session.query(User).filter(User.email==session['email']).first()
        lipa=MpesaExpress()
        stkpush=lipa.stk_push(amount="500",phone_number=phone_num.phone)
            #time.sleep()
        if stkpush["ResponseCode"]=="0":
            time.sleep(2)
            flash("Activation fee payment request has been sent to your number")
            mpepe=Mpesax(session['email'],"500", "0", date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), CheckoutRequestID=stkpush["CheckoutRequestID"])
            commit_data(mpepe)
            return redirect(url_for('confirm',amount=500,request_id=stkpush["CheckoutRequestID"],status="0",**request.args))
        else:
            flash("Failed Payment Operation")
                    
    return render_template('activate.html',account_status =active())


@app.route('/confirm_payment/<request_id>/<amount>/<status>',methods =["GET","POST"])
def confirm(amount=None,request_id=None,status=None):
    if amount and request_id and status:
        amount_sent=amount
        requested_id=request_id
        state=status
        #print(amount_sent,requested_id,state)
    else:
        flash("Can not Confirm payment")
    if request.method =="POST":
        activate_acc=db.session.query(Activate).filter(Activate.email==session['email']).first()
        RequestID=db.session.query(Mpesax).filter(Mpesax.email==session['email'],Mpesax.CheckoutRequestID==requested_id,Mpesax.status==state,Mpesax.amount==amount_sent).first()
        lipa=MpesaExpress()
        check_stkpush=lipa.query(checkout_request_id=RequestID.CheckoutRequestID)
        #check_stkpush=lipa.query(checkout_request_id="ws_CO_010220221355142049")
        if check_stkpush["ResultCode"]== "0":
            #wallet.wallet_ammount=int(wallet.wallet_ammount)+ int(amount_sent)
            activate_acc.status="ACTIVATED"
            RequestID.status="1"
            db.session.commit()
            return redirect("/dashboard")

        else:
            RequestID.status=check_stkpush["ResultDesc"]
            db.session.commit()
            flash(check_stkpush["ResultDesc"])

        
    return render_template("mpesa.html",account_status =active())




@app.route('/credentials',methods =["GET","POST"])
def mpepe():
    return render_template('mpesa.html')          
if __name__ == '__main__':
    app.run()