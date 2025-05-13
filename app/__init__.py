# Handles app creation and configuration
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect 
from app.config import *

# Initialise extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()  # Create a login manager object
login_manager.login_view = (
    "auth.login"  # Set the login view to 'login' for redirecting unauthenticated users
)

# Create the Flask application
def create_app(isTest=False):
    flaskApp = Flask(__name__)
    if isTest:
        flaskApp.config.from_object(TestConfig)
    else:
        flaskApp.config.from_object(DeploymentConfig)
    
    # Init extensions with the app
    db.init_app(flaskApp)
    migrate.init_app(flaskApp, db)
    csrf.init_app(flaskApp)  # Initialize CSRF protection with the app
    login_manager.init_app(flaskApp)  # Initialize the login manager with the app
    
    # Register blueprints and routes
    from app.routes import main as main_blueprint
    flaskApp.register_blueprint(main_blueprint)
    
    from app.routes_auth import auth as auth_blueprint
    flaskApp.register_blueprint(auth_blueprint)
    
    return flaskApp