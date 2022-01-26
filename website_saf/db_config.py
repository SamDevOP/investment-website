
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from models import *
#from app import db

def creating_user(email,phone,passcode,referal_code,db):
    try:
        user=User(email = email,phone = phone,passcode = passcode,referal_code=referal_code)
        db.session.add(user)
        db.session.commit()
        return "User added. book id={}".format(user.id)
    except Exception as e:
	    return(str(e))
