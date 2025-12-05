from flask import Flask, request, render_template, redirect
import os, pymysql

app=Flask(__name__)

db_conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="RootPass@123",
    database="employees"
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name=request.form['name']
    email=request.form['email']
    role=request.form['role']
    cur=db_conn.cursor()
    cur.execute("INSERT INTO employees (name,email,role) VALUES (%s,%s,%s)",(name,email,role))
    db_conn.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
