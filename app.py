# app.py is server file
# import email
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

# configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES(%s,%s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    RESULT = cur.execute(
        "SELECT * FROM  USERS")
    if RESULT > 0:
        userDetails = cur.fetchall()
        return render_template("users.html", userDetails=userDetails)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        name = userDetails['name']
        cur = mysql.connection.cursor()
        cur.execute(
            "delete from users where name= '%s' " % (name))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('delete.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute(
            "update users set name=%s where email=%s", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)
