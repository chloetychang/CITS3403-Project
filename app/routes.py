from flask import render_template
from app import app

@app.route('/')

@app.route('/home')
def home():
    return "Hello, World!"

@app.route('/visualisation')
def visualisation():
    return "Hello, Visualisation!"

@app.route("/share")
def share():
    return "Hello, Share!"