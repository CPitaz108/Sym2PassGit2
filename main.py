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

# Import Flask and Flask_Restful's API, Resource

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
import time
import math
import json

##Create a Flash object called API with the parameter __name__ (Name of the python file)
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1001494'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'sympass'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

##Access-Control-Allow-Origin, has vunlnerablities so will have to look into changes for this later.
CORS(app)


##Creats a API object called API from the Flash object
##This was a cross-orgin function test, remove later
##@app.route("/test")
##def helloWorld():
#    return "Hello, cross-origin-world!"


##This was a test to check if the database can return the tables information, will be removed
@app.route('/users/getall')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM customers;''')
    rv = cur.fetchall()
    return str(rv)


##This was an early test on getting a users device id, though we have not yet found a way to fully implement yet.
@app.route('/users/get_user_by_device/<device_id>')
def get_user_by_device(device_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(device_id) + "\'")
    rv = cur.fetchall()
    return str(rv)


##we request the feed information that should be the customers usernames and status.
@app.route('/users/get_feed')
def get_user_feed():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM customers;''')
    rv = cur.fetchall()
    x = json.dumps(rv)
    return str(x)


##Here we are getting all the needed information from the clinics db that we will use to populate the map
@app.route('/geo/get_clinics')
def get_clinics_address():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM customers;''')
    rv = cur.fetchall()
    x = json.dumps(rv)
    return str(x)


##This is the foundation code for the symp2pass test page. All information here will soon be organized to update in order.
##The main changes to this function is the order in which the data is input.
@app.route('/user/d_id=<d_id>&epc=<epc_id>')
def add(d_id, epc_id):
    cur = mysql.connection.cursor()
    # cur.execute('''SELECT MAX(id) FROM customers;''')
    # maxID = cur.fetchone()
    user_id = 0
    seconds = math.floor(time.time())
    expire_time = seconds + 120
    # valid_until = seconds+86400
    cur.execute("INSERT INTO customers (name,epc,id,expire_time,seconds) VALUES (%s, %s, %s, %s, %s)",
                (d_id, epc_id, user_id, expire_time, seconds))
    # cur.execute('''INSERT INTO customers(name,epc)''', (name, epc_id))##maxID['MAX(id)'] + 1 (maxID['MAX(id)'] + 1, device_id, valid_until, expire_time, seconds, test_status, test_id, epc_id)
    # mysql.connection.commit()
    # <br>\nid: " + str(maxID['MAX(id)'] + 1) + "<br>\ndevice_id: " + str(device_id) + "<br>\nVerification Endtime: " + str(valid_until) + "<br>\nTime scan is active: " + str(expire_time) + "<br>\nLast Updated: " + str(seconds) + "<br>\nTest Status: " + str(test_status) + "<br>\nTest ID: " + str(test_id) + "<br>\nEPC ID: " + str(epc_id)
    status = "Inserted the following row:" + "device_id" + d_id + " epc_id:" + epc_id + \
             " Seconds:" + str(seconds) + " ExpireTime: " + str(expire_time) + "<br>" + str(user_id)
    print(status)
    x = "completed"
    w = str(x)
    return w


##This is the Client form input function. Here we get the form data from the site and insert it into the the db
@app.route('/upload/new_user/data=<data>')
def upload_form(data):
    ##We turn the json file into something more readable for the API
    y = json.loads(data)
    ##Then set up a connection to the mysql server
    cur = mysql.connection.cursor()
    ##We ask the server for the max client value
    curr_client_max = cur.execute('''SELECT * FROM clients;''')
    ##Then we insert all the values from the json file into the database.
    cur.execute(
        "INSERT INTO clients (id_clients,business_client_name,address_client,city_client,state_province_client,zip_post_client,country_client,operation_time_client,days_of_operation_client,"
        "loc_type_client,phone_client,email_client,website_client,emergency_contact_client,notes_client)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (curr_client_max + 1, y["data"]["business_name"], y["data"]["address_1"], y["data"]["city"],
         y["data"]["Province_State"], y["data"]["postal_zip"], y["data"]["country"], y["data"]["operation_hours"],
         y["data"]["days_of_operation"], y["data"]["loc_type"], y["data"]["phone"], y["data"]["email"],
         y["data"]["web"], y["data"]["e_contact"], str(y["data"]["notes"])))
    ##We then commit our changes to the server
    mysql.connection.commit()
    ##Currently we have a response to check if the script ran, though we will not need this later
    response = "Thank you for your input " + str(y["data"]["business_name"]) + "<br>" + "user number " + str(
        curr_client_max)
    return response


##This is the qr code validator. Here we are checking to see if the scanned QR code exist or has unfinished test sections.
@app.route('/test/epc_valid/id=<in_qr_id>')
def sent_valid(in_qr_id):
    print("Checking epc id")
    cur = mysql.connection.cursor()
    # This preforms an sql search for a already existing value
    cur.execute("SELECT * FROM customers WHERE  epc =" + in_qr_id)
    ##Since we can not get a T/F value back we instead count the number of rows that exist with the value
    ##If we get a row count that is >0 then we know the value exist in the db
    row_count = cur.rowcount
    if row_count == 0:
        print("This epc does not exist")
        w = "false"
    else:
        print("This epc already exist")
        w = "true"
    # print("number of affected rows: {}".format(row_count))
    ##We then send a T/F value back to the site that the javascript can read
    return w


##Here is the smell test solver. We have it solving in the API in hopes to decrease the ability of trying to cheat.
@app.route('/test/scentsible_solver/answer=<answer>&s_id=<s_id>')
def check_sent_answer(answer, s_id):
    interdict = {"c7a4476fc64b75ead800da9ea2b7d072": "cherry",
                 "67c0ecaf5a1b782b11146e9fbe80f016": "lime",
                 "495bf9840649ee1ec953d99f8e769889": "strawberry",
                 "b781cbb29054db12f88f08c6e161c199": "grape",
                 "3f24e567591e9cbab2a7d2f1f748a1d4": "lemon"}
    correct_answer = interdict[str(answer)]
    u_answer = s_id.lower()
    user_ID = ''
    if u_answer == correct_answer:
        w = "correct"
    else:
        w = "incorrect"
    print(str("Correct Answer: " + correct_answer))
    print("User(" + user_ID + ") Answer: " + u_answer)
    print("Result: " + w)
    ##x = str(correct_answer+"<br>" + u_answer + "<br>" + w + "<br> User:"+s_id)
    x = str(w)
    return x


##Passes
@app.route('/passes/get_status/<device_id>')
def get_status_by_device(device_id):
    cur = mysql.connection.cursor()
    seconds = math.floor(time.time())
    cur.execute('''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(
        device_id) + "\'" + '''AND valid_until > ''' + str(seconds) + ''' ORDER BY valid_until DESC''')
    rv = cur.fetchone()
    if rv == ():
        return "No Valid Pass!"
    return "Valid Pass Found: " + str(rv)


@app.route('/passes/get_status_history/<device_id>')
def get_status_history_by_device(device_id):
    cur = mysql.connection.cursor()
    seconds = math.floor(time.time())
    cur.execute(
        '''SELECT * FROM customers WHERE device_id = ''' + "\'" + str(device_id) + "\' ORDER BY valid_until DESC")
    rv = cur.fetchall()
    if rv == ():
        return "No Passes Found!"
    return "Passes Found: " + str(rv)


##If the function is the main.py (Which this is)
if __name__ == "__main__":
    app.run(debug=True)
