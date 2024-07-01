from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os
app=Flask(__name__)

#flask initialization
app.secret_key = os.getenv('SECRET_KEY')

#mysqlconfiguration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']=os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'crudforaxce'

#mysql initialization
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, lastname, email FROM users")
    users = cur.fetchall()
    session['users'] = users
    cur.close()

    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        
        # Insert into table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s)", (firstname, lastname, email))
        mysql.connection.commit()
        
        # Fetch the updated list of jobs
        cur.execute("SELECT id, firstname, lastname, email FROM users")
        users = cur.fetchall()
        session['users'] = users
        cur.close()
        
        return redirect(url_for('home'))

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()

    cur.execute("SELECT id, firstname, lastname, email FROM users")
    users = cur.fetchall()
    session['users'] = users
    cur.close()

    return redirect(url_for('comprofile',id=session['id']))


if  __name__ == '__main__':
    app.run(debug = True)