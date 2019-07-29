from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal

#access your device page here.it is for status also.
# @app.route("/get_pc_data")
@app.route("/yourdevice")
@app.route("/status")
def downloadpowerandcurrent():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from(select * from consumption order by id desc limit 10)var order by id asc")
    powerandcurrentdata=list(curso.fetchall())
    power=[]
    current=[]
    now=[]
    for i in powerandcurrentdata:
        power.append(i[3])
        current.append(i[4])
        now.append(i[2])
    graph = pygal.Line(x_label_rotation=30)
    graph.title = 'power consumption data'
    graph.x_labels = (str(now[0]),str(now[1]),str(now[2]),str(now[3]),str(now[4]),str(now[5]),str(now[6]),str(now[7]),str(now[8]),str(now[9]))
    graph.add('Power', [int(float(power[0])),int(float(power[1])),int(float(power[2])),int(float(power[3])),int(float(power[4])),int(float(power[5])),int(float(power[6])),int(float(power[7])),int(float(power[8])),int(float(power[9]))])
    g1=graph.render_data_uri()
    date=powerandcurrentdata[0][1]
    graph1 = pygal.Line(x_label_rotation=30)
    graph1.title = 'current consumption data'
    graph1.x_labels = (str(now[0]),str(now[1]),str(now[2]),str(now[3]),str(now[4]),str(now[5]),str(now[6]),str(now[7]),str(now[8]),str(now[9]))
    graph1.add('Current', [int(float(current[0])),int(float(current[1])),int(float(current[2])),int(float(current[3])),int(float(current[4])),int(float(current[5])),int(float(current[6])),int(float(current[7])),int(float(current[8])),int(float(current[9]))])
    g2=graph1.render_data_uri()
    connec.close()
    return render_template( 'yourdevice.html', g1=g1,g2=g2,powerandcurrentdata=powerandcurrentdata,date=date)


@app.route("/yourdevice2")
@app.route("/status")
def youdevice2():
    onoffdetails=setonoff()
    print(onoffdetails)
    return render_template("statistics.html",onoffdetails=onoffdetails)


#calls statistics page.
@app.route("/statistics")
def statistics_page():
    return render_template("statistics.html")


#gives access to faq page.
@app.route("/faq")
def faq_page():
    return render_template("faq.html")

#does signout and returns home_before_log page.
@app.route("/signout")
def signout():
    return render_template("home_before_log.html")





