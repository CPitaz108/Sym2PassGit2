# Buy bracelet with a QR code, scan the code which brings them to a website.
#
# On that website, the QR code will redirect them to the website with an EPC value (Unique Primary Key).
#
# ID is recorded along with timestamp, (test done/expired), timestamp on how long the bracelet is active. To refresh you would rescan the QR code. Cookie create that reauuthenticates
#
# WTF Forms and Flask using python to code the route (MicroWSGI). GET would tell them whether or not they have scanned, redirect to the verification page. POST info to the API, get them an access key for the DB
#
# Run flask locally, then have him set up and deploy the web server in the cloud. EPC and Row ID, Phone ID, EPC (QR Tag ID), Three timestamps (Long Lived Verification, Short Lived Verification, When they were updated).
#
# 80% coverage for unit testing is what he is looking for.

#Import Flask and Flask_Restful's API, Resource
from flask import Flask;
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with;
from flask_mysqldb import MySQL;
from flask_sqlalchemy import SQLAlchemy;

##Create a Flash object called API with the parameter __name__ (Name of the python file)
app = Flask(__name__);
##Creats a API object called API from the Flash object
api = Api(app);
app.config()

##Test class that defines a HelloWorld object. By defining the class HelloWorld, you can give it methods (A get method has already been established that
# just returns a sample JSON object with a data key, and a value of "Hello World"
class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World"};
##You can def PUT, def POST, def PATCH, GET, DELETE. to define other methods for this class that you may want (For updating an entire field, inserting, updating a single field, getting data from the DB, and removing records
# respectively)

##This is called at the very end and actually adds the resource (A HelloWorld class object) to the API using the provided URL suffix ("/helloworld").
# The general syntax to call it would be "[URL]/api/helloworld")
api.add_resource(HelloWorld, "/helloworld")


##If the function is the main.py (Which this is)
if __name__ == "__main__":
    app.run(debug=True);