# Buy bracelet with a QR code, scan the code which brings them to a website.
#
# On that website, the QR code will redirect them to the website with an EPC value (Unique Primary Key).
#
# ID is recorded along with timestamp, (test done/expired), timestamp on how long the bracelet is active. To refresh you would rescan the QR code. Cookie create that reauuthenticates
#
# WTF Forms and Flask using python to code the route (MicroWSGI). GET would tell them whether or not they have scanned, redirect to the verification page. POST info to the API, get them an access key for the DB
#
# Run flask locally, then have him set up and deploy the web server in the cloud. EPC and Row ID, Phone ID, EPC (QR Tag ID), Three timestamps (Long Lived Verification, Short Lived Verification, When they were updated).
# 80% coverage for unit testing is what he is looking for.

#Import Flask and Flask_Restful's API, Resource

from flask import Flask;
from flask_restful import Api, Resource;
from flask_mysqldb import MySQL;
import time;
import math;

##Create a Flash object called API with the parameter __name__ (Name of the python file)
app = Flask(__name__);

app.config['MYSQL_USER'] = 'root';
app.config['MYSQL_PASSWORD'] = '1234';
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'sympass'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app);
##Creats a API object called API from the Flash object

@app.route('/users/getall')
def get_users():
    cur = mysql.connection.cursor();
    cur.execute('''SELECT * FROM customers;''');
    rv = cur.fetchall();
    return str(rv);

@app.route('/users/get_user_by_device/<device_id>')
def get_user_by_device(device_id):
    cur = mysql.connection.cursor();
    cur.execute('''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(device_id) + "\'");
    rv = cur.fetchall();
    return str(rv);

@app.route('/user/epc=<epc_id>&d=<device_id>&t_id=<test_id>&s=<test_status>')
def add(epc_id, device_id, test_id, test_status):
    cur = mysql.connection.cursor();
    cur.execute('''SELECT MAX(id) FROM customers;''');
    maxID = cur.fetchone();
    seconds = math.floor(time.time());
    expire_time = seconds+120;
    valid_until = seconds+86400;
    cur.execute('''INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (maxID['MAX(id)'] + 1, device_id, valid_until, expire_time, seconds, test_status, test_id, epc_id));
    mysql.connection.commit();
    status = "Inserted the following row: <br>\nid: " + str(maxID['MAX(id)'] + 1) + "<br>\ndevice_id: " + str(device_id) + "<br>\nVerification Endtime: " + str(valid_until) + "<br>\nTime scan is active: " + str(expire_time) + "<br>\nLast Updated: " + str(seconds) + "<br>\nTest Status: " + str(test_status) + "<br>\nTest ID: " + str(test_id) + "<br>\nEPC ID: " + str(epc_id);
    print(status);
    return status

##Passes
@app.route('/passes/get_status/<device_id>')
def get_status_by_device(device_id):
    cur = mysql.connection.cursor();
    seconds = math.floor(time.time());
    cur.execute('''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(device_id) + "\'" + '''AND valid_until > ''' + str(seconds) + ''' ORDER BY valid_until DESC''');
    rv = cur.fetchone();
    if rv == ():
        return "No Valid Pass!"
    return "Valid Pass Found: " + str(rv);

@app.route('/passes/get_status_history/<device_id>')
def get_status_history_by_device(device_id):
    cur = mysql.connection.cursor();
    seconds = math.floor(time.time());
    cur.execute('''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(device_id) + "\' ORDER BY valid_until DESC");
    rv = cur.fetchall();
    if rv == ():
        return "No Passes Found!"
    return "Passes Found: " + str(rv);

##Test class that defines a HelloWorld object. By defining the class HelloWorld, you can give it methods (A get method has already been established that
# just returns a sample JSON object with a data key, and a value of "Hello World"
# class HelloWorld(Resource):
#     def get(self):
#         return {"data": "Hello World"};
# ##You can def PUT, def POST, def PATCH, GET, DELETE. to define other methods for this class that you may want (For updating an entire field, inserting, updating a single field, getting data from the DB, and removing records
# # respectively)
#
# ##This is called at the very end and actually adds the resource (A HelloWorld class object) to the API using the provided URL suffix ("/helloworld").
# # The general syntax to call it would be "[URL]/api/helloworld")
# api.add_resource(HelloWorld, "/helloworld")
#
#
##If the function is the main.py (Which this is)
if __name__ == "__main__":
    app.run(debug=True);