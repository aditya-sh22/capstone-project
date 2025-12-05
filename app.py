from flask import Flask, request, render_template, redirect
import os
import pymysql
import time

app = Flask(__name__)

# ----------- DB CONNECTION WITH RETRIES -------------
def get_db():
    return pymysql.connect(
        host=os.getenv("DBHOST"),
        port=int(os.getenv("DBPORT")),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPWD"),
        database=os.getenv("DATABASE"),
        cursorclass=pymysql.cursors.DictCursor
    )

def connect_with_retry():
    retries = 10
    while retries > 0:
        try:
            conn = get_db()
            print("Connected to MySQL successfully!")
            return conn
        except Exception as e:
            print("MySQL not ready - retrying...")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to MySQL after several attempts")

# Single reusable connection for startup checks
db_conn = connect_with_retry()

# ------------------- ROUTES -----------------------
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO employees (name, email, role) VALUES (%s, %s, %s)",
        (name, email, role)
    )
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/employees')
def view_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    conn.close()
    return render_template("employees.html", employees=rows)

# ---------------- RUN APP -------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
