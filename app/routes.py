from flask import render_template
from app import app

@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html', title="Home")

@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html', title = "Visualisation")

@app.route("/share")
def share():
    return render_template('share.html', title = "Share")
