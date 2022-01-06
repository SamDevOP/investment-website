#from werkzeug import secure_filename
import re
from flask import Flask,render_template,request,redirect,url_for,flash,session
import os
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from sqlqueries import *
#from mpesa_views import *
from datetime import datetime,timedelta




#Initializing flask app
app=Flask(__name__)

Base_URL="http://localhost:5000/signup/"

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1AHEKSpdsr'

@app.route('/',methods =["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        phonenum=request.form["email"]
        passcode=request.form["password"]
        login_user()
        for each in login_user.records:
                    #print(each[1],each[2])
            session['email']=each[0]
                
            if phonenum==each[0] and passcode==each[2]:
                #print(phonenum,passcode)
                session['response']=each[0]
                #generate_refer_code()
                return redirect('/dashboard')
            else:
                flash("Email or Password not correct!")
    return render_template('login.html')


@app.route('/signup',methods =["GET","POST"])
@app.route('/signup/<referral_code>',methods =["GET","POST"])
def signup(referral_code=None):
    if referral_code:
        referral_c = referral_code
    if request.method== "POST":
        mail=request.form["email"]
        phone=request.form["phone"]
        
            #add a fetch all to chech for emails and phone duplication
        root_pass=request.form["password"]
        repeat_pass=request.form["cpassword"]
            
        if root_pass != repeat_pass:
            flash('Passwords Don\'t match')
        else:
            if len(root_pass)<8:
                flash("Your Password should be more than 8 Characters")
            else:
                r_code=generate_refer_code(mail,phone)
                ref_code=[]
                check_codes=retrieve_user_refcode()
                for all in check_codes:
                    ref_code.append(all[0])
                    
                if referral_c in ref_code:
                    insert_referals_earned((mail,r_code,referral_c,200))
                    wallet_email=retrieve_user_email(referral_c)[0]
                    r_wallet=int(retrieve_wallet(wallet_email)[0])
                    new_wallet=r_wallet + 200
                    update_wallet((new_wallet,wallet_email))

                create_user((mail,phone,root_pass,r_code))
                wallet = 0
                insert_wallet((mail,wallet))

                flash("Account created Successfully!")
                return redirect("/login")

        
    return render_template('signup.html')


@app.route('/dashboard',methods =["GET","POST"])
def dashboard():
    retrieve_transactions(session['email'])
    fund_transactions(session['email'])
    my_records= retrieve_transactions.records
    if my_records==[]:
        amount_invested= 0
        expected_income=  0
        invest_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        maturitydate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        maturity_date= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time_remaining=0
    else:
        for all in my_records:
            if all[1]=='Invested' and all[4]>all[3]:
                amount_invested=all[2]
                if amount_invested==0:
                    expected_income=0
                else:
                    expected_income=amount_invested + (amount_invested*0.4)  
                invest_date=all[3]
                maturitydate = all[4]
                maturity_date= datetime.strptime(maturitydate, '%d/%m/%Y %H:%M:%S')
                #wallet=all[5]
                #time_remaining= datetime.now()
    
                if maturity_date < datetime.now():
                    time_remaining = 'Your transaction is complete'
                else:
                    time_remaining = maturity_date - datetime.now()
        
    wallet = retrieve_wallet(session['email'])[0]


            

    return render_template('dashboard_home.html',my_records=my_records,expected_income=expected_income,\
        amount_invested=amount_invested,maturity_date=maturity_date,invest_date=invest_date,time_remaining=time_remaining,wallet=wallet)
    #downloads = os.path.join(current_app.root_path,'')
    #return send_from_directory(directory=downloads,filename='decrypted.txt', as_attachment=True)
@app.route('/referrals',methods =["GET","POST"])
def refer():

    referral_link=Base_URL+retrieve_referal_code(session['email'])
    
    return render_template('refer.html',referral_link=referral_link)


@app.route('/withdraw',methods =["GET","POST"])
def withdraw():
    if request.method == "POST":
        withdrawn_cash = int(request.form["withdraw_cash"])
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        wallet=int(retrieve_wallet(session['email'])[0])
        withdraw_cash = withdrawn_cash + 30
        if withdraw_cash>wallet:
            flash("Your transaction cannot be completed due to insufficient Funds")
        else:
            wallet = wallet - withdraw_cash
            update_wallet((wallet,session['email']))
            flash("Withdrawn " + str(withdrawn_cash) + " Cost of Transaction: 30" )

    return render_template('withdraw.html')  

@app.route('/fund',methods =["GET","POST"])
def fund():
    if request.method == "POST":
        fund_cash = request.form["fund_cash"]
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        #add Mpesa transaction information here

        wallet=retrieve_wallet(session['email'])[0]

        wallet = int(wallet) + int(fund_cash)
        update_wallet((wallet,session['email']))
        flash("Your account has been credited with " + str(fund_cash))
        # insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
    return render_template('fund_acct.html')

@app.route('/invest',methods =["GET","POST"])
def invest():
    if request.method == "POST":
        fund_cash = request.form["fund_cash"]
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        maturity_date=(datetime.now() + timedelta(hours=72)).strftime("%d/%m/%Y %H:%M:%S")
        fund_transactions(session['email'])
        my_data = fund_transactions.records
        for all in my_data:
            wallet=all[4]
        
        retrieve_transactions(session['email'])
        record =retrieve_transactions.records
        if record==[]:
            insert_transactions((session['email'],'Filler',0,the_date,maturity_date))
        else:
            insert_transactions((session['email'],'Invested',fund_cash,the_date,maturity_date))
            flash("You have invested " + str(fund_cash))
            wallet=int(wallet)-int(fund_cash)
            update_wallet((wallet,session['email']))
        # insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
    return render_template('invest.html')    
    
@app.route('/credentials',methods =["GET","POST"])
def mpepe():
    return render_template('mpesa.html')          
if __name__ == '__main__':
    
    app.run()