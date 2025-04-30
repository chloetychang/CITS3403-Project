from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # can potentially add more fields - such as age, public/private profile, etc.

class Entry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    sleep_datetime = db.Column(db.DateTime, nullable=False)
    wake_datetime = db.Column(db.DateTime, nullable=True)
    mood = db.Column(db.Integer, nullable=True)       # mood - indexed for future calculations
    created_at = db.Column(db.DateTime, nullable=True)
    last_modified = db.Column(db.DateTime, nullable=True)