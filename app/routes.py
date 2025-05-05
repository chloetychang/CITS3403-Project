# Contains routing logic
from flask import render_template, redirect, url_for, session, flash
from app import app
from app.forms import LoginForm, SignupForm, UploadSleepDataForm  # Import forms
from datetime import datetime
from app.models import db, User, Entry  # Import models from database

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
        new_user.password = form.password.data  # uses setter and hashes password
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
def sleep():
    if "user_id" not in session:
        return redirect(url_for("login"))
    form = UploadSleepDataForm()                            # Create an instance of the UploadSleepDataForm
    return render_template("sleep.html", form=form)

@app.route("/form_popup", methods=["POST"])
def form_popup():
    form = UploadSleepDataForm()
    if form.validate_on_submit():
        # Get the user ID from flask-login
        user_id = current_user.user_id
        entry_date_sleep = form.entry_date_sleep.data
        sleep_time = form.sleep_time.data
        entry_date_wake = form.entry_date_wake.data
        wake_time = form.wake_time.data
        
        sleep_datetime = datetime.combine(entry_date_sleep, sleep_time)
        wake_datetime = datetime.combine(entry_date_wake, wake_time) if entry_date_wake and wake_time else None
        
        # Check if the sleep time is before the wake time
        if wake_datetime and sleep_datetime >= wake_datetime:
            flash("Unsuccessful Submission - Sleep time must be before wake time.", "error")
            return render_template("sleep.html", form=form)
        
        # Check if the sleep time is in the future
        if sleep_datetime > datetime.now():
            flash("Unsuccessful Submission - Sleep time cannot be in the future.", "error")
            return render_template("sleep.html", form=form)
        
        # Check if the wake time is in the future
        if wake_datetime and wake_datetime > datetime.now():
            flash("Unsuccessful Submission - Wake time cannot be in the future.", "error")
            return render_template("sleep.html", form=form)
        
        # Create a new entry instance - fields as defined in forms.py
        new_entry = Entry(
            user_id = user_id,
            sleep_datetime = sleep_datetime,
            wake_datetime = wake_datetime,                  # Optional
            mood = form.mood.data
        )
        db.session.add(new_entry) # Add the new entry to the session
        db.session.commit()  # Save the new entry to the database
        
        flash("Sleep data recorded successfully!", "success")
        return redirect(url_for("sleep"))  # Redirect to sleep page after successful submission
        
    return render_template("sleep.html", form=form)
        
@app.route("/record")
def record():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("record.html")


@app.route("/results")
def results():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("results.html")
