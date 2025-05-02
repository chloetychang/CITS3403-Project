from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable = False)
    username = db.Column(db.String(60), unique = True, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(22), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)    # hashed password
    

class Entry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    sleep_datetime = db.Column(db.DateTime, nullable=False)
    wake_datetime = db.Column(db.DateTime, nullable=True)
    mood = db.Column(db.Integer, nullable=True)       # mood - indexed for future calculations
    # sleep duration - calculated from sleep and wake datetime (field not required here)
    # sleep quality - calculated from mood and sleep duration (field not required here)