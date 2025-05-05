# Contains routing logic
from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.forms import LoginForm, SignupForm, UploadSleepDataForm  # Import forms
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SignupForm, UploadSleepDataForm  # Import forms
from datetime import datetime
from app.models import db, User, Entry  # Import models from database
from flask_login import current_user, login_user, logout_user, login_required

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Create an instance of the LoginForm
    if form.validate_on_submit(): # Check if the form is submitted and valid
        # Check if the email exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Store user info in session
            session['user_id'] = user.user_id
            session['user_name'] = user.name

            flash("Logged in successfully!", "success")
            return redirect(url_for('sleep'))   # redirect to sleep page after successful login
        else:
            flash("Invalid email or password.", "error")

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Create an instance of the SignupForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        # Check if the email already exists in the database
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash("Email already registered", "error")
            return redirect(url_for('signup'))

        # Check if the username already exists in the database
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        if existing_user_username:
            flash("Username already taken", "error")
            return redirect(url_for('signup'))

        # Create a new user instance to add to the database
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            age=form.age.data,
            gender=form.gender.data,
            email=form.email.data,
        )

        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Save the new user to the database

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login page after successful signup

    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()  # Log the user out using Flask-Login
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route("/sleep")
@login_required # Protected page - added decorator to ensure user is logged in
def sleep():
    # Check if the user is logged in using Flask-Login
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("login"))
    form = UploadSleepDataForm()                            # Create an instance of the UploadSleepDataForm
    return render_template("sleep.html", form=form)


@app.route("/record")
@login_required # Protected page
def record():
    # Check if the user is logged in using Flask-Login
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("login"))
    return render_template("record.html")


@app.route("/results")
@login_required # Protected page
def results():
    # Check if the user is logged in using Flask-Login
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("login"))
    return render_template("results.html")
