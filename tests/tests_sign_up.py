import unittest
from app import create_app, db
from app.models import User, Entry
from app.forms import SignupForm
from app.config import TestConfig
from werkzeug.datastructures import MultiDict

class TestSignUp(unittest.TestCase):
    def setUp(self):
        """ Called before every test method """
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """ Called after every test method """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_creation_password_hashing(self):
        """ 
        Test that a user can be created, the password is hashed and not stored in plain text 
        To run test: python -m unittest tests.tests_sign_up.TestSignUp.test_user_creation_password_hashing
        """
        user = User(name="Pingu", username="pingu", age="5", gender="Male", email="nootnoot@example.com")
        user.password = "ahhhh_glorious_fish"
        db.session.add(user)
        db.session.commit()
        
        retrieved = User.query.filter_by(username="pingu").first()
        self.assertIsNotNone(retrieved)
        self.assertNotEqual(retrieved.password_hash, "ahhhh_glorious_fish")          # Check password is hashed
        self.assertTrue(retrieved.check_password("ahhhh_glorious_fish"))             # Check password validation
        self.assertIsInstance(retrieved.password_hash, str)                          # Check if password_hash is a string            
        self.assertTrue(retrieved.password_hash.startswith("pbkdf2:sha256:"))        # Check Werkzeug hash format
        
    def test_successful_signup(self):
        """
        Test that a user can be created with valid data.
        To run test: python -m unittest tests.tests_sign_up.TestSignUp.test_successful_signup
        """
        form_entry = SignupForm(formdata=MultiDict({
            "name": "Skipper", 
            "username": "definitely_unique_user", 
            "age": 35,
            "gender": "male",
            "email": "skipper@example.com",
            "password": "penguins_are_cool",
            "confirm_password": "penguins_are_cool"
        }))
        self.assertIsNotNone(form_entry.name.data)
        self.assertIsNotNone(form_entry.username.data)
        self.assertIsNotNone(form_entry.age.data)
        self.assertIsNotNone(form_entry.gender.data)
        self.assertIsNotNone(form_entry.email.data)
        self.assertIsNotNone(form_entry.password.data)
        self.assertIsNotNone(form_entry.confirm_password.data)
        self.assertTrue(form_entry.validate())
    
    def test_invalid_email(self):
        """
        Test that a user cannot be created with an invalid email.
        To run test: python -m unittest tests.tests_sign_up.TestSignUp.test_invalid_email
        """
        form_entry = SignupForm(formdata=MultiDict({
            "name": "Slacker", 
            "username": "definitely_unique_user", 
            "age": 20, 
            "gender": "male", 
            "email": "skipperisaslacker", 
            "password": "I_wanna_be_like_Skipper",
            "confirm_password": "I_wanna_be_like_Skipper"
        }))
        self.assertFalse(form_entry.validate())
        self.assertIn("Please enter a valid email address", form_entry.email.errors)
    
    def test_password_length(self):
        """
        Test that a user cannot be created with a password shorter than 6 characters.
        To run test: python -m unittest tests.tests_sign_up.TestSignUp.test_password_length
        """
        form_entry = SignupForm(formdata=MultiDict({
            "name": "Peppa", 
            "username": "peppa_pig", 
            "age": 4, 
            "gender": "female", 
            "email": "peppa@pig.com", 
            "password": "count",
            "confirm_password": "count"
        }))
        self.assertFalse(form_entry.validate())
        self.assertIn("Field must be at least 6 characters long.", form_entry.password.errors)