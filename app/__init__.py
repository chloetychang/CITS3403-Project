# Handles app creation and configuration
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

app = Flask(__name__, static_folder="static")
app.config.from_object(Config)  # Configure the `app` object using our `Config` class
db = SQLAlchemy(app)  # Create SQLAlchemy object called db
migrate = Migrate(app, db)  # Create a migrate object

login_manager = LoginManager()  # Create a login manager object
login_manager.init_app(app)  # Initialize the login manager with the app
login_manager.login_view = (
    "login"  # Set the login view to 'login' for redirecting unauthenticated users
)

app.secret_key = "monke-magic"  # REMINDER to not include secret key in final version.

if __name__ == "__main__":
    app.run()

from app import routes, models
