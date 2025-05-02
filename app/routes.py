# Contains routing logic
from flask import render_template, redirect, url_for, session, request, flash
from app import app
from app.forms import LoginForm, SignupForm  # Import forms
from app.mock_data import users  # Replace users with real database later
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instantiate the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        email = form.email.data
        password = form.password.data
        user = users.get(email)
        # Check if users exist and password matches
        if user and check_password_hash(user["password"], password):
            session["user"] = {"email": email, "name": user["name"]}
            flash("Login successful!", "success")
            return redirect(url_for("sleep"))
        # If the user does not exist or password does not match, show an error message
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))
    # If the request method is GET or the form is not valid, render the login template
    return render_template("login.html", form=form)  # Pass the form to the template


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()  # Instantiate the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        name = form.name.data
        username = form.username.data
        age = form.age.data
        gender = form.gender.data
        email = form.email.data
        password = form.password.data
        # Check if email already exists
        if email in users:
            flash("Email already exists", "error")
        # Check if username is already used (search all users)
        elif any(user["username"] == username for user in users.values()):
            flash("Username already taken", "error")
        # Create a new user
        else:
            users[email] = {
                "name": name,
                "username": username,
                "age": age,
                "gender": gender,
                "password": generate_password_hash(password, method="pbkdf2:sha256"),
            }
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
    # If the request method is GET or the form is not valid, render the signup template
    return render_template("signup.html", form=form)  # Pass the form to the template


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("welcome"))


# Protected routes
@app.route("/sleep")
def sleep():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("sleep.html")


@app.route("/record")
def record():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("record.html")


@app.route("/results")
def results():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("results.html")
