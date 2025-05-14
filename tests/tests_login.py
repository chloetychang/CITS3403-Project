import unittest
from app import create_app, db
from app.models import User, Entry
from app.forms import LoginForm
from app.config import TestConfig

class TestLogin(unittest.TestCase):
    def setUp(self):
        """ Called before every test method """
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data_to_db()
    
    def tearDown(self):
        """ Called after every test method """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def add_test_data_to_db(self):
        users = [
            User(name="Skipper", username="skipper", age="35", gender="Male", email="skipper@example.com"),
            User(name="Private", username="private", age="14", gender="Male", email="private@example.com"),
            User(name="Rico", username="rico", age="32", gender="Male", email="rico@example.com"),
            User(name="Kowalski", username="kowalski", age="35", gender="Male", email="kowalski@example.com")
        ]
        for user in users:
            user.password = "penguins_are_cool"
            db.session.add(user)
            
        db.session.commit()