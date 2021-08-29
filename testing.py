from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://beatkraq:1436@3.36.88.26', 27017) 
db = client.dbtest2

account = db.infofs.find_one({'user':'connection12'} and {'pswd':'Bee4answer*'})

if account != None:
    print(account)
else:
    print('No info')