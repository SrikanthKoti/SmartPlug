from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal
############################PAGE ACCESS METHODS########################

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

######################################PERSON DATA PROCESS METHODS############################

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

##################################################POWER CONSUMPTION DATA TAKERS TO WEBSITE####################

#this is in your_device.html page.FOR GRAPH.
# @app.route("/")
@app.route("/get_pc_data")
def get_pc_data():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from(select * from consumption order by id desc limit 10)var order by id asc")
    powerandcurrentdata=list(curso.fetchall())
    power=[]
    current=[]
    time=[]
    for i in powerandcurrentdata:
        power.append(i[3])
        current.append(i[4])
        now=str(i[2])
        time.append(now[:-7])
    connec.close()
    return render_template("yourdevice.html",p=power,c=current,t=time)

#in statistics page.check statistics by date.
@app.route("/checkbydate",methods=['GET','POST'])
def checkbydate():
    submittype=request.form['submittype']
    print(submittype)
    if submittype=="checkdata":
        power=0
        current=0
        startdate=request.form['fromdate']
        finaldate=request.form['todate']
        connec=mysql.connect()
        curso=connec.cursor()
        curso.execute("select power,current from consumption where date between (%s) and (%s)",(startdate,finaldate))
        data=curso.fetchall()
        print(data)
        for i in data:
            power=power+i[0]
            current=current+i[1]
            print(data)
        connec.close()
        return render_template("statistics.html",power=power,current=current)
    elif submittype=="downloaddata":
        startdate=request.form['fromdate']
        finaldate=request.form['todate']
        connec=mysql.connect()
        curso=connec.cursor()
        curso.execute("select * from consumption where date between (%s) and (%s)",(startdate,finaldate))
        data=curso.fetchall()
        with open("power_and_current_data.csv",'a') as f1:
           writer=csv.writer(f1)
           writer.writerow(('s.no','date','time','power','current'))
           for i in data:
               writer.writerow(i)
        connec.close()
        return render_template("statistics.html")
    else:
        connec=mysql.connect()
        curso=connec.cursor()
        curso.execute("select * from consumption")
        data=curso.fetchall()
        with open("all_power_and_current_data.csv",'a') as f2:
           writer=csv.writer(f2)
           writer.writerow(('s.no','date','time','power','current'))
           for i in data:
               writer.writerow(i)
        connec.close()
        return render_template("statistics.html")

#check schedule of your device.
@app.route("/checkschedule",methods=['GET','POST'])
def checkschedule():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select starttime,endtime from schedule")
    data=curso.fetchall()
    deviceSchedule='Your Device is Scheduled From'+str(data[0][0])[:-3]+' To '+str(data[0][1])[:-3]
    workingtime='Your Device Is Working For '+str(data[0][1]-data[0][0])[:-3]+" Hours "
    connec.close()
    return render_template("statistics.html",deviceSchedule=deviceSchedule,workingtime=workingtime)


###############################DATA UPLOADING FROM WEBSITE TO DATABASE##########################

#in statistics page.set schedule.
@app.route("/setschedule",methods=['POST'])
def setschedule():
    start=request.form['starttime']
    end=request.form['endtime']
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("Update schedule set starttime = (%s) ,endtime=(%s) Where id = 1",(start,end))
    connec.commit()
    connec.close()
    return render_template("statistics.html")

#update on or off.
@app.route("/setonoff")
def setonoff():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from onoff")
    data=curso.fetchall()
    curso.close()
    curso=connec.cursor()
    print(data)
    if data[0][1] == 0:
        curso.execute("Update onoff set onoff=(%s) Where id = 1",1)
        connec.commit()
        onoffdetails="Your Device Was ON Now"
    else:
        curso.execute("Update onoff set onoff=(%s) Where id = 1",0)
        connec.commit()
        onoffdetails="Your Device Was OFF Now"
    return onoffdetails

#######################################DATA UPLOAD FROM ARDUINO TO DATABASE#######################
#upload current values dynamically.
@app.route("/")
@app.route("/upload_pc_data_dinamic")
def upload_pc_data_dinamic():
    connec=mysql.connect()
    curso=connec.cursor()
    for i in range(0,10):
        power=randint(0,19)
        current=randint(0,19)
        presentdate=date.today()
        presenttime=datetime.now().time()
        curso.execute("insert into consumption(date,time,power,current) values (%s,%s,%s,%s)",(presentdate,presenttime,power,current))
        connec.commit()
    return "successfully uploaded"
         #
         #
         #
       ######
        ###
         #

#upload current values from arduino.
@app.route("/upload_pc_data",methods=['GET'])
def upload_pc_data():
    power=request.args.get('power')
    current=request.args.get('current')
    # power=float(powerandcurrent[:-4])
    # current=float(powerandcurrent[:4])
    connec=mysql.connect()
    curso=connec.cursor()
    format = "%H:%M:%S"
    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    print(now_utc.strftime(format))
    # Convert to Asia/Kolkata time zone
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    presenttime=now_asia.strftime(format)
    presentdate=date.today()
    curso.execute("insert into consumption(date,time,power,current) values (%s,%s,%s,%s)",(presentdate,presenttime,power,current))
    connec.commit()
    connec.close()
    return "successfully uploaded"


#################################NODEMCU TAKING VALUES FROM WEBSITE TO DATABASE#####################


@app.route("/getschedulevalue")
def getschedulevalues():
    format = "%H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    presenttime=now_asia.strftime(format)
    print(presenttime)
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from schedule")
    data=curso.fetchall()
    if datetime.strptime(presenttime,"%H:%M:%S") > datetime.strptime(str(data[0][1]),"%H:%M:%S") and datetime.strptime(presenttime,"%H:%M:%S") < datetime.strptime(str(data[0][2]),"%H:%M:%S"):

        return "1"
    else:
        return "0"

@app.route("/getonoffvalue")
def getonoffvalues():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from onoff")
    data=curso.fetchall()
    connec.close()
    if data[0][1]==1:
        return "1"
    else:
        return "0"
###############Android Studio########

@app.route("/androidgetgraphdata")
def androidgetgraphdata():
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select * from(select * from consumption order by id desc limit 10)var order by id asc")
    powerandcurrentdata=list(curso.fetchall())
    power=[]
    current=[]
    time=[]
    now=[]
    connec.close()
    for i in powerandcurrentdata:
        power.append(i[3])
        current.append(i[4])
        now.append(str(i[2]))
        # time.append(now[:-7])
    data=power+current+now
    return render_template("empty.html",data=data)

@app.route("/androidgetscheduledata",methods=['GET'])
def androidgetscheduledata():
    starttime=request.args.get('timestart')
    finaltime=request.args.get('timeend')
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("Update schedule set starttime = (%s) ,endtime=(%s) Where id = 1",(starttime,finaltime))
    connec.commit();
    connec.close()
    return "Successfull"

@app.route("/androidgetstatisticsdata",methods=['GET'])
def androidgetstatisticsdata():
    power=0.0
    current=0.0
    startdate=request.args.get('startdate')
    finaldate=request.args.get('finaldate')
    connec=mysql.connect()
    curso=connec.cursor()
    curso.execute("select power,current from consumption where date between (%s) and (%s)",(startdate,finaldate))
    data=curso.fetchall()
    connec.close()
    for i in data:
        if(i[0]==None or i[1]==None):
            continue;
        power=power+float(str(i[0]))
        current=current+float(str(i[1]))
    dot="Power : "+str(round(power,3))+"<br>Current : "+str(round(current,3))
    return dot
