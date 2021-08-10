from flask import Flask, jsonify, request
from flask_cors import CORS,cross_origin
from pymongo import MongoClient
import urllib 
from bson.json_util import dumps
import Config

username = urllib.parse.quote_plus(Config.USERNAME)
password = urllib.parse.quote_plus(Config.PASSWORD)
cluster = urllib.parse.quote_plus(Config.CLUSTER)
database = urllib.parse.quote_plus(Config.DATABASE)


url = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(username, password, cluster, database)

client = MongoClient(url)
db = client.get_database('BigMagic')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():  
    return("Welcome to Flask-Monogo Code Snippet")

@app.route('/userSignUp', methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def userSignUp():
    records = db.userdetails

    # userDetails = request.get_json()
    # email = userDetails['Email']

    email = "karishma@gmail.com"
    userDetails = {
        'Name': "Karishma Dasgaonkar",
        'Email': "karishma@gmail.com",
        'Password': '1234'
    }

    response = dumps(records.find_one({'Email': email}))
    print(response)

    if (response == 'null' ):
        response = records.insert_one(userDetails)
        print(response)
        return ("Document Inserted")
    else:
        return ("False")
        


@app.route('/userSignIn', methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def userSignIn():

    records = db.userdetails
    #TODO: Hash Password before storing or find a better strategy
      
    # userDetails = request.get_json()
    # email = userDetails['Email']
    # pasd = userDetails['Password']

    email = "karishma@gmail.com"
    pasd = '1234'

    response = dumps(records.find_one({'Email': email, 'Password':pasd}))
    print(response)

    if (response):
        return response
    else:
        return ("False")


@app.route('/userUpdateData', methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def userUpdateData():

    records = db.userdetails
    
    filter = { 'Email': 'meghnani.bhavya@gmail.com' }
    
    # Values to be updated.
    newvalues = { "$set": { 'Password': '5678' } }
    
    # Using update_one() method for single value
    response = records.update_one(filter, newvalues)

    print(response)


    if (response):
        return "Document Updated"
    else:
        return ("False")


app.run(port=5000, debug=True)