from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'monke-magic'  # change key for production, honestly not sure how this works, please review and implement securely.

# Mock database (replace with real DB later i.e. db that stores username and pw data.)
users = {
    "test@example.com": {
        "password": generate_password_hash("password123", method='pbkdf2:sha256'),  # ← Explicit method
        "name": "Test User"
    }
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users.get(email)
        
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'email': email,
                'name': user['name']
            }
            flash('Login successful!', 'success')
            return redirect(url_for('sleep'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')  # Ensure this points to login.html


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            flash('Email already exists.', 'error')
        else:
            users[email] = {
                'password': generate_password_hash(password, method='pbkdf2:sha256'),
                'name': name
            }
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')  # Ensure this points to signup.html

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Protected Routes, comment them out as needed if you want to access without login.
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

if __name__ == '__main__':
    app.run(debug=True)