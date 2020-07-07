#!/usr/bin/python
#coding=utf-8

## script to run flask application, main backend for website
## written by joey shepin

from flask_mysqldb import MySQL
from flask import Flask,render_template,request
app=Flask(__name__)
mysql=MySQL(app)

## initial attributes for flask app

app.config['SECRET_KEY']='secret!'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='garageapp'
app.config['MYSQL_PASSWORD']='nega5897'
app.config['MYSQL_DB']='shshacks2020'
app.config['MYSQL_CURSORCLASS']='DictCursor'

## main routes of application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('fullMap.html')


#gets data from client-side form, queries database for relevant data,
#returns data to client
@app.route('/get_data',methods=['GET','POST'])
def getData():
    zipCode=request.form['zipCode']
    print("ZIP CODE IS "+zipCode)
    cur=mysql.connection.cursor()
    cur.execute("SELECT * from data WHERE zipcode = %s",(zipCode,))
    data=cur.fetchone()
    return data

##run server

if __name__=='__main__':
    app.secret_key='secret123'
    app.run(host='0.0.0.0',port=3003,threaded=True,debug='True')
