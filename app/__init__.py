# Handles app creation and configuration

from flask import Flask

app = Flask(__name__, static_folder='static')
app.secret_key = 'monke-magic'                  # reminder to not include secret key in final version.
    
if __name__ == "__main__":
    app.run()

from app import routes