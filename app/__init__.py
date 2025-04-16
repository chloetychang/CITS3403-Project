from flask import Flask
app = Flask(__name__, template_folder='templates/html', static_folder='app/static')

if __name__ == "__main__":
    app.run()
    
from app import routes