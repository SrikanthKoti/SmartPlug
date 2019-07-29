from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal

#during subscribe.need flash.
@app.route("/subscribe",methods=['POST'])
def subscribe():
    subemail=request.form['subsemail']
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from subscription where email=(%s)",(subemail))
    subscribeEmailCount=curso.fetchall()
    if len(subscribeEmailCount)==0:
        curso.execute("insert into subscription(email) values (%s)",(subemail))
        connec.commit()
        connec.close()
        return "Thank's for SUBSCRIBING US"
    else:
        return "YOU HAD ALDREADY SUBSCRIBED US."

#contact submission.
@app.route("/contactus",methods=['POST'])
def contactus():
    email=request.form['email']
    name=request.form['name']
    comment=request.form['comments']
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("insert into contactus(name,email,comment) values (%s,%s,%s)",(name,email,comment))
    connec.commit()
    connec.close()
    flash("successfully sent")
    return "Successfully SENT"
