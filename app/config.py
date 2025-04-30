import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location
    SECRET_KEY = "penguin-magic"