# Contains routing logic

from flask import render_template, redirect, url_for, session, request, flash
from app import app
from app.mock_data import users                 # Replace users with real database later
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users.get(email)
        
        # Check if users exist and password matches
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'email': email,
                'name': user['name']
            }
            flash('Login successful!', 'success')
            return redirect(url_for('sleep'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))   # avoid resubmitting form 
        
    return render_template('login.html')        # only loads form on GET
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username', '').strip()
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users:
            flash('Email already exists', 'error')
        else:
            users[email] = {
                'name': name,
                'password': generate_password_hash(password, method='pbkdf2:sha256'),
                'username': username,
                'age': age,
                'gender': gender
                
            }
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
    return render_template('signup.html')       # Ensure this points to signup.html

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('welcome'))

# Protected routes
@app.route('/sleep')
def sleep():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('sleep.html')

@app.route('/record')
def record():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('record.html')

@app.route('/results')
def results():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('results.html')