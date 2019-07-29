from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal
#calls home_befor_log.

@app.route("/")
@app.route("/home")
@app.route("/home_befor_log")
def home_b_l():
    return render_template("home_before_log.html")

#gives access to login page.

@app.route("/login")
def login():
    return render_template("login.html")

#gives access to register page.

@app.route("/register")
def register():
    return render_template("register.html")

#gives access to home_after_log page.

@app.route("/home_after_log")
def home_a_l():
    return render_template("home_after_log.html")


