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


UPLOAD_FOLDER = 'docs/'
ALLOWED_EXTENSIONS = ['pdf', 'txt','docx']

#Initializing flask app
app=Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER


app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1AHEKSpdsr'

# def allowed_file(filename,ALLOWED_EXTENSIONS):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods =["GET","POST"])
def upload_dashboard():
    if request.method== "POST":
        checking=request.form.get('terms_conditions')
        keep=request.form.get('keep')

        if checking == 'on':
            mail=request.form["mail"]
            phone=request.form["phone"]
            #add a fetch all to chech for emails and phone duplication
            root_pass=request.form["root_pass"]
            repeat_pass=request.form["repeat_pass"]
            if root_pass != repeat_pass:
                flash('Passwords Don\'t match')
            else:
                if len(root_pass)<8:
                    flash("Your Password should be more than 8 Characters")
                else:
                    create_user((mail,phone,root_pass))
                    #pass

        #log in
        elif keep=='on' or keep=='off':    
            phonenum=request.form["phonenum"]
            passcode=request.form["passcode"]
            login_user()
            for each in login_user.records:
                #print(each[1],each[2])
                session['email']=each[0]
              
                if phonenum==each[0] and passcode==each[2]:
                    #print(phonenum,passcode)
                    session['response']=each[0]
                    return redirect('/dashboard')
                else:
                    flash("Number or Password not correct!")
        #print(passcode,phonenum)
        #login_user()
        

        
        #email = request.form["gall"]

        # if 'pic' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)

        # doc = request.files["pic"]
        #doc=doc.save(secure_filename(doc.filename))
        #name=session['email']

        # if doc.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if doc and allowed_file(doc.filename,ALLOWED_EXTENSIONS):
        #     fileName = secure_filename(doc.filename)
        #     doc.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        #     docpath = UPLOAD_FOLDER + fileName

        
            

    return render_template('login_register.html')
# @app.route('/download')
# def download():
#     downloads = os.path.join(current_app.root_path,'')
#     return send_from_directory(directory=downloads,filename='encrypted.txt', as_attachment=True)


@app.route('/dashboard',methods =["GET","POST"])
def dashboard():
    # if request.method== "POST":
    #     fund_cash=request.form.get('fund_cash')
    #     print(fund_cash)
    #     phonenumber=254798766620 #session['response']
    #     my_c2b=C2B()
    #     my_c2b.simulate(shortcode=600988,command_id='CustomerPayBillOnline',amount=fund_cash,msisdn=phonenumber)
    #     #return render_template('dashboard.html')
    #     flash("Your account has been credited")
    retrieve_transactions(session['email'])
    my_records= retrieve_transactions.records

    for all in my_records:
        if all[1]=='Fund Account' and all[4]>all[3]:
            amount_invested=all[2]
            expected_income=amount_invested + (amount_invested*0.4)  
            invest_date=all[3]
            maturitydate = all[4]
            maturity_date= datetime.strptime(maturitydate, '%d/%m/%Y %H:%M:%S')
            #time_remaining= datetime.now()
   
            if maturity_date < datetime.now():
                time_remaining = 'Your transaction is complete'
            else:
                time_remaining = maturity_date - datetime.now().strftime("%d/%m/%Y %H:%M:%S")



            

    return render_template('dashboard_home.html',my_records=my_records,expected_income=expected_income,\
        amount_invested=amount_invested,maturity_date=maturity_date,invest_date=invest_date,time_remaining=time_remaining)
    #downloads = os.path.join(current_app.root_path,'')
    #return send_from_directory(directory=downloads,filename='decrypted.txt', as_attachment=True)
@app.route('/referrals',methods =["GET","POST"])
def refer():
    return render_template('refer.html')


@app.route('/withdraw',methods =["GET","POST"])
def withdraw():
    if request.method == "POST":
        withdraw_cash = request.form["withdraw_cash"]
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_transactions((session['email'],'Withdrawal',withdraw_cash,the_date))
        flash("Withdrawn " + str(withdraw_cash))
    return render_template('withdraw.html')  

@app.route('/fund',methods =["GET","POST"])
def fund():
    if request.method == "POST":
        fund_cash = request.form["fund_cash"]
        the_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        maturity_date=(datetime.now() + timedelta(hours=48)).strftime("%d/%m/%Y %H:%M:%S")
        retrieve_transactions(session['email'])
        record =retrieve_transactions.records
        for all in record:
            if all[1]=='Fund Account' and all[4]>all[3]:
                flash("You have a live transaction")
            else:
                insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
                flash("Your account has been credited with " + str(fund_cash))
        # insert_transactions((session['email'],'Fund Account',fund_cash,the_date,maturity_date))
    return render_template('fund_acct.html')          
if __name__ == '__main__':
    
    app.run()