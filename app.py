from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(_name_)
app.secret_key = 'secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gym_db"
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", 
                       (request.form['username'], request.form['password']))
        user = cursor.fetchone()
        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        plan = request.form['plan']
        status = request.form['status']
        cursor.execute("INSERT INTO members (name, phone, plan, payment_status) VALUES (%s, %s, %s, %s)", 
                       (name, phone, plan, status))
        db.commit()
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    return render_template('dashboard.html', members=members)

@app.route('/update/<int:id>')
def update_payment(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("UPDATE members SET payment_status = IF(payment_status='Pending', 'Clear', 'Pending') WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if _name_ == '_main_':
    app.run(debug=True)