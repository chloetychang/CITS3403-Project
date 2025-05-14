import unittest
from app import create_app, db
from app.models import User, Entry
from app.forms import LoginForm
from app.config import TestConfig
from werkzeug.datastructures import MultiDict

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
            User(name="Skipper", username="skipper", age="35", gender="male", email="skipper@example.com"),
            User(name="Private", username="private", age="14", gender="male", email="private@example.com"),
            User(name="Rico", username="rico", age="32", gender="male", email="rico@example.com"),
            User(name="Kowalski", username="kowalski", age="35", gender="male", email="kowalski@example.com")
        ]
        for user in users:
            user.password = "penguins_are_cool"
            db.session.add(user)
            
        db.session.commit()
        
    def test_successful_login(self):
        """
        Test that a user can log in with valid credentials.
        To run test: python -m unittest tests.tests_login.TestLogin.test_successful_login
        """
        form_entry = LoginForm(formdata=MultiDict({
            "email":"skipper@example.com",
            "password":"penguins_are_cool"
        }))
        self.assertIsNotNone(form_entry.email.data)
        self.assertIsNotNone(form_entry.password.data)
        self.assertTrue(form_entry.validate())
    
    def test_login_validation(self):
        """
        Test that users can only log in with all required fields filled in.
        To run test: python -m unittest tests.tests_login.TestLogin.test_login_validation
        """
        form_entry = LoginForm(formdata=MultiDict({
            "email":"skipper@example.com"
        }))
        self.assertFalse(form_entry.validate())
        self.assertIn("This field is required.", form_entry.password.errors)