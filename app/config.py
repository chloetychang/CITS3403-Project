import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') # Configures the secret key for the app
    
class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    SECRET_KEY = 'test-secret-key'
    TESTING = True
    WTF_CSRF_ENABLED = False