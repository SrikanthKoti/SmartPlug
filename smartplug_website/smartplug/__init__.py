from flask import Flask

from flaskext.mysql import MySQL


app=Flask(__name__)
#for flash messages.
app.secret_key="dont"
#for connection to database.
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sriki007$iot-smart-plug'
mysql=MySQL(app)


from smartplug import login_and_register_routes
from smartplug import web_routes
from smartplug import website_to_database_routes
from smartplug import yourdevice_routes
from smartplug import other_routes 