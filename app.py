from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
from bson import json_util
from datetime import date
import smtplib
import os
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json

app = Flask(__name__)

client = MongoClient('mongodb://beatkraq:1436@3.36.88.26', 27017) 
db = client.dbtest2
app.secret_key='whateveritis'
s = URLSafeTimedSerializer(app.secret_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('register.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/loggedin')
def loggedin():
    return render_template('loggedin.html')


@app.route('/register', methods=['POST'])
def post_information():
    
    email_receive = request.form.get('email_give')
    pswd_receive = request.form.get('pswd_give')
    user_receive = request.form.get('user_give')
    month_receive = request.form.get('month_give')
    day_receive = request.form.get('day_give')
    year_receive = request.form.get('year_give')

    account = db.infofs.find_one({'user':user_receive})
    if account != None:
        block = 'block'
        return render_template('register.html', error=block)
    else:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        information = {'email': email_receive,'pswd': pswd_receive,'user': user_receive,'month': month_receive,'day': day_receive,'year': year_receive}

        db.informations.insert_one(information)

        token = s.dumps(user_receive)
        confirm_email = render_template('email.html', token=token)

        msg = EmailMessage()
        msg['Subject'] = 'PUBG Global Account Activation (Replica)'
        msg['From'] = "stanfm95@gmail.com"
        msg['To'] = email_receive
        msg.set_content('Confirmation please')

        msg.add_alternative(confirm_email, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login("stanfm95@gmail.com", os.getenv('pswd1'))
            smtp.send_message(msg)

        return render_template("verification.html", email=email_receive, pswd= pswd_receive, user=user_receive, month=month_receive, day=day_receive, year=year_receive, d1=d1)

@app.route('/temporary', methods=['POST'])
def resend_email():
    email_receive = request.form['email_give']
    pswd_receive = request.form['pswd_give']
    user_receive = request.form['user_give']
    month_receive = request.form['month_give']
    day_receive = request.form['day_give']
    year_receive = request.form['year_give']
    
    token = s.dumps(user_receive)
    confirm_email = render_template('email.html', token=token)

    msg = EmailMessage()
    msg['Subject'] = 'PUBG Global Account Activation: Resent (Replica)'
    msg['From'] = "stanfm95@gmail.com"
    msg['To'] = email_receive
    msg.set_content('Confirmation please')

    msg.add_alternative(confirm_email, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login("stanfm95@gmail.com", os.getenv('pswd1'))
        smtp.send_message(msg)

    return jsonify({'result': 'success'})

@app.route('/confirmation/<token>')
def confirm_email(token):
    try:
        user_receive = s.loads(token, max_age=3600)
    except SignatureExpired:
        return False
    return render_template('confirmation.html', user=user_receive)

@app.route('/confirmed_info', methods=['GET', 'POST'])
def save_information():
    user_receive = request.form['user_give']
    infof = db.informations.find_one({'user':user_receive}, {'_id': 0})

    db.infofs.insert_one(infof)

    return jsonify({'result': 'success'})

@app.route('/authentication', methods=['POST'])
def login_validation():
    user_receive = request.form.get('user_give')
    pswd_receive = request.form.get('pswd_give')

    account = db.infofs.find_one({'user':user_receive} and {'pswd':pswd_receive})
    if account != None:
        return render_template('loggedin.html')
    else:
        block = 'block'
        return render_template('index.html', error=block)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)