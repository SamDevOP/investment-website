#from werkzeug import secure_filename
import email
from math import remainder
import re
from traceback import StackSummary
from flask import Flask,render_template,request,redirect,url_for,flash,session
import os
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from sqlqueries import *
from mpesa_views import *
from datetime import datetime,timedelta
import base64




#Initializing flask app
app=Flask(__name__)

Base_URL="https://peakinvestors-app.herokuapp.com/"

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1AHEKSpdsr'

@app.route('/',methods =["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        phonenum=request.form["email"]
        passcode=request.form["password"]
        login_user()
        emails=[]
        for each in login_user.records:
            emails.append(each[0])
        if phonenum not in emails:
            flash("The email doesn't exist")
        else:
            password=retrieve_password(phonenum)
            session['email']=phonenum
            if passcode==password:
                return redirect('/dashboard')
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
            
        if root_pass != repeat_pass:
            flash('Passwords Don\'t match')
        else:
            if len(root_pass)<8:
                flash("Your Password should be more than 8 Characters")
            else:
                username_check=retrieve_username()
                if username in username_check:
                    flash("Username exists. Choose another.")
                else:
                    #r_code=generate_refer_code(mail,phone)
                    if len(phone)!=12:
                        flash("Mpesa phone number is incorrect. Format is: 2547XXXXXXXX")
                    else:
                        ref_code=[]
                        check_codes=retrieve_user_refcode()
                        for all in check_codes:
                            ref_code.append(all[0])
                        if referral_c!='':    
                            if referral_c in ref_code:
                                insert_referals_earned((mail,username,referral_c,200))
                                wallet_email=retrieve_user_email(referral_c)[0]
                                r_wallet=int(retrieve_wallet(wallet_email)[0])
                                new_wallet=r_wallet + 200
                                update_wallet((new_wallet,wallet_email))
                        
                        #rootpass=root_pass.encode("utf-8")
                        #encoded_rootpass=base64.b64encode(rootpass)
                        create_user((mail,phone,root_pass,username))
                        wallet = 0
                        insert_wallet((mail,wallet))
                        insert_activate((mail,username,"DEACTIVATED"))

                        flash("Account created Successfully!")
                        return redirect("/login")  
    return render_template('signup.html')


@app.route('/dashboard',methods =["GET","POST"])
def dashboard():
    #retrieve_transactions(session['email'])
    #fund_transactions(session['email'])
    if session["email"]=="":
        return redirect(url_for('login'))

    else:

        my_records= retrieve_investing(session['email'])
        wallet = int(retrieve_wallet(session['email']))
        if len(my_records)==0:
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
                maturitydate = all[2]
                maturity_date= datetime.strptime(maturitydate, '%d/%m/%Y %H:%M:%S')
                time_remaining = maturity_date - datetime.now()
                if time_remaining.total_seconds()<=0:
                    update_investing(('Done',session['email'],all[7]))
                else:  
                    update_investing(('Live',session['email'],all[7]))

            if all[4]=="Live" and all[6]=="NO":
                total_invested.append(all[1])
                total_revenue.append((int(all[1]) + ((int(all[1])*0.4))))

            if all[4] == "Done" and all[6]=="NO":
                value = wallet + (int(all[1]) + ((int(all[1])*0.4)))
                update_wallet((value,session['email']))
                update_investing_added_wallet(("YES",session['email']))
            
                remaining_time.append(time_remaining.total_seconds())
            expected_income=sum(total_revenue)
            amount_invested=sum(total_invested)
    
        
    
        total_referals=len(retrieve_referals_numbers(retrieve_referal_code(session['email'])))
        wallet = int(retrieve_wallet(session['email'])[0])
        


    return render_template('dashboard_home.html',my_records=my_records,expected_income=expected_income,\
        amount_invested=amount_invested,remaining_time=time_remaining,wallet=wallet,total_referals=total_referals)
    


@app.route('/referrals',methods =["GET","POST"])
def refer():

    referral_link=Base_URL+retrieve_referal_code(session['email'])
    
    return render_template('refer.html',referral_link=referral_link)


@app.route('/withdraw',methods =["GET","POST"])
def withdraw():
    if request.method == "POST":
        withdrawn_cash = int(request.form["withdraw_cash"])
        #the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        wallet=int(retrieve_wallet(session['email'])[0])

        status=retrieve_activate(session['email'])[0]

        if status == "DEACTIVATED":
            flash("Activate account to be able to invest")
        else:
            if int(withdrawn_cash)<=1500:
                transaction_cost=30
            elif int(withdrawn_cash)>1500:
                transaction_cost=50

            withdraw_cash = withdrawn_cash + transaction_cost
            if withdraw_cash>wallet:
                flash("Your transaction cannot be completed due to insufficient Funds")
            else:
                wallet = wallet - withdraw_cash
                update_wallet((wallet,session['email']))
                flash("Withdrawn " + str(withdrawn_cash) + " Cost of Transaction: "+ str(transaction_cost) )

    return render_template('withdraw.html')  

@app.route('/fund',methods =["GET","POST"])
def fund():
    if request.method == "POST":
        fund_cash = request.form["fund_cash"]
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if len(retrieve_wallet(session['email']))>0:
            wallet=retrieve_wallet(session['email'])[0]
        
        #add Mpesa transaction information here
        phone=retrieve_user_phone(session['email'])
        
        status=retrieve_activate(session['email'])[0]

        if status == "DEACTIVATED":
            flash("Activate account to be able to invest")
        else:
            lipa=MpesaExpress()
            stkpush=lipa.stk_push(amount=str(fund_cash),phone_number=phone)
            time.sleep(5)
            if "ResponseCode" in stkpush:
                if stkpush["ResponseCode"] ==  "0":
                    flash("Payment request has been sent to your number")
                else:
                    flash("Payment request failed. Try again later")
            else:
                flash("Payment request failed. Try again later")
            for i in range(1,100):
                check_stkpush=lipa.query(checkout_request_id=stkpush["CheckoutRequestID"])
                #check_stkpush=lipa.query(checkout_request_id="ws_CO_190120220940204345")
                if "ResultCode" in check_stkpush:

                    if check_stkpush["ResultCode"]!="0":
                        continue
                    else:
                        #insert_mpesa((session['email'],fund_cash,stkpush["CheckoutRequestID"],"SUCCESS",the_date))
                        wallet = int(wallet) + int(fund_cash)
                        update_wallet((wallet,session['email']))
                        flash("Your account has been credited with " + str(fund_cash))
                        break
                        
                else:
                    flash("An error occured. Refresh Page and try again.")#insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
    return render_template('fund_acct.html')

@app.route('/invest',methods =["GET","POST"])
def invest():
    if request.method == "POST":
        
        fund_cash = request.form["fund_cash"]
        investment_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date=datetime.now().strftime("%d/%m/%Y")
        maturity_date=(datetime.now() + timedelta(hours=72)).strftime("%d/%m/%Y %H:%M:%S") #(hours=72)
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        the_date=datetime.strptime(the_date, '%d/%m/%Y %H:%M:%S').date()
        inv_id='INV'

        if session['email'] == "":
            return redirect(url_for('login'))
        else:

            my_data = retrieve_investing(session['email'])
            

            wallet=int(retrieve_wallet(session['email'])[0])

            if len(my_data)==0:
                inv_id=inv_id + str(len(my_data))
                if int(fund_cash)> int(wallet):
                    flash("You have insufficient balance to complete the investment")
                    return redirect('/fund')
                else:
                    insert_investing((session['email'],fund_cash,maturity_date,investment_date,'Live',date,'NO',inv_id))
                    wallet=int(wallet)-int(fund_cash)
                    update_wallet((wallet,session['email']))
                    flash("You have invested " + str(fund_cash))
                    
            else:
                if len(select_number_of_inv(("Live",str(date))))<=2:
                    
                    if int(fund_cash)> int(wallet):
                        flash("You have insufficient balance to complete the investment")
                        return redirect('/fund')
                    else:
                        inv_id=inv_id + str(len(my_data))
                        insert_investing((session['email'],fund_cash,maturity_date,investment_date,'Live',date,'NO',inv_id))
                        wallet=int(wallet)-int(fund_cash)
                        update_wallet((wallet,session['email']))
                        flash("You have invested " + str(fund_cash))
                else:
                    flash("You have exhausted today \'s investment opportunities")
    return render_template('invest.html')    

"""============================================ACTIVATE ACCOUNT======================"""
# @app.route('/activate',methods =["GET","POST"])
# def activate():
#     acc_status=retrieve_activate(session['email'])[0]
#     phone=retrieve_user_phone(session['email'])
    
#     if acc_status=="DEACTIVATED":
#         status="0"
#     else:
#         status="1"
#     return render_template("activate.html",status=status)




@app.route('/activate',methods =["GET","POST"])
def activate():
    if len(retrieve_activate(session['email']))>0:
        acc_status=retrieve_activate(session['email'])[0]
    if acc_status=="DEACTIVATED":
        status="0"
    else:
        status="1"
    if request.method == "POST":
        #status="3"
        phone=retrieve_user_phone(session['email'])
        
        if acc_status=="DEACTIVATED":
            lipa=MpesaExpress()
            stkpush=lipa.stk_push(amount="500",phone_number=phone)
            #time.sleep()
            if stkpush["ResponseCode"]=="0":
                flash("Activation fee payment request has been sent to your number")
            #time.sleep(35)
            for i in range(1,100):
                check_stkpush=lipa.query(checkout_request_id=stkpush["CheckoutRequestID"])
                if "errorCode" not in check_stkpush:
                    if check_stkpush["ResultCode"]!="0":
                        #flash("Account not activated. Try again ")
                        status="0"
                        time.sleep(2)
                        continue
                    else:
                        status="1"
                        update_activate(("ACTIVATED",session['email']))
                        time.sleep(2)
                        flash("Account activated.")
                        #time.sleep(2)
                        #return redirect('/dashboard')
                        break

                
    return render_template('activate.html',status=status)



@app.route('/credentials',methods =["GET","POST"])
def mpepe():
    return render_template('mpesa.html')          
if __name__ == '__main__':
    
    app.run()