from flask import flash,request,render_template,Response,redirect,session,url_for
from smartplug import app
from smartplug import mysql
import time
from pytz import timezone
from datetime import date,datetime,timedelta
from random import randint
import csv
import pygal

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
