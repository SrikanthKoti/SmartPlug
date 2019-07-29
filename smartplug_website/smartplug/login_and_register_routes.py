from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal

#during log in.
@app.route("/check",methods=['POST'])
def check():
    email=request.form['email']
    password=request.form['password']
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from authenticate where email=(%s) and password=(%s)",(email,password))
    emailCorrectCount=curso.fetchall()
    if len(emailCorrectCount)==1:
        Login="OK"
        connec.close()
        return render_template("home_after_log.html")
    else:
        connec.close()
        return "pls check user name or password"

#during register.need flash.
@app.route("/insert",methods=['POST'])
def insert():
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    repassword=request.form['repeatpassword']
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from authenticate where email=(%s)",(email))
    emailCount=curso.fetchall()
    connec.close()
    if not(len(password)==0) and (password==repassword):
        if len(emailCount) == 0:
            curso.execute("insert into authenticate(Name,Email,Password) values (%s,%s,%s)",(username,email,password))
            connec.commit()
            flash("oh! god you registered")
            flash("now goto home")
            Login="OK"
            connec.close()
            return render_template("layout.html")
        else:
            connec.close()
            return "<h1>YOU ALDREADY REGISTERED</h1>"
    else:
        return '<H1>CHECK YOUR PASSWORD</H1>'


