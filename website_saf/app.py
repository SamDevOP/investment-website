#from werkzeug import secure_filename
import re
from flask import Flask,render_template,request,redirect,url_for,flash,session
import os
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
#from sqlqueries import *


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

        if checking == 'on':
            mail=request.form["mail"]
            phone=request.form["phone"]
            root_pass=request.form["root_pass"]
            repeat_pass=request.form["repeat_pass"]
            if root_pass != repeat_pass:
                flash('Passwords Don\'t match')
            else:
                if len(root_pass)<8:
                    flash("Your Password shoould be more than 8 Characters")
                else:
                    #create_user((mail,phone,root_pass))
                    pass

        else:
            phonenum=request.form["phonenum"]
            passcode=request.form["passcode"]
            print(passcode,phonenum)
            return redirect('/dashboard')

        
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

        
            

    return render_template('upload.html')
# @app.route('/download')
# def download():
#     downloads = os.path.join(current_app.root_path,'')
#     return send_from_directory(directory=downloads,filename='encrypted.txt', as_attachment=True)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    #downloads = os.path.join(current_app.root_path,'')
    #return send_from_directory(directory=downloads,filename='decrypted.txt', as_attachment=True)
            
if __name__ == '__main__':
    
    app.run()