from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.forms import LoginForm, SignupForm                         # Import forms
from app.models import db, User                                     # Import models from database


auth = Blueprint('auth', __name__)

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Create an instance of the LoginForm
    if form.validate_on_submit(): # Check if the form is submitted and valid
        # Check if the email exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Store user info in session
            login_user(user)  # Log the user in using Flask-Login

            flash("Logged in successfully!", "success")
            return redirect(url_for('main.sleep'))   # redirect to sleep page after successful login
        else:
            flash("Invalid email or password.", "error")

    return render_template('login.html', form=form)


# Signup Route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Create an instance of the SignupForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        # Check if the email already exists in the database
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash("Email already registered", "error")
            return redirect(url_for('auth.signup'))

        # Check if the username already exists in the database
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        if existing_user_username:
            flash("Username already taken", "error")
            return redirect(url_for('auth.signup'))

        # Create a new user instance to add to the database
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            age=form.age.data,
            gender=form.gender.data,
            email=form.email.data,
        )
        new_user.password = form.password.data 

        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Save the new user to the database

        flash("Account created successfully!", "success")
        return redirect(url_for('auth.login'))  # Redirect to login page after successful signup

    return render_template('signup.html', form=form)


# Logout Route
@auth.route('/logout')
def logout():
    logout_user()  # Log the user out using Flask-Login
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
