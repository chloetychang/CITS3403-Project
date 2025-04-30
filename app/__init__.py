# Handles app creation and configuration

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)                  # Configure the `app` object using our `Config` class
db = SQLAlchemy(app)                            # Create SQLAlchemy object called db
migrate = Migrate(app, db)                      # Create a migrate object

app.secret_key = 'monke-magic'                  # reminder to not include secret key in final version.
    
if __name__ == "__main__":
    app.run()

from app import routes, models