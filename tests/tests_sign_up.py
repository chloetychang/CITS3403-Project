import unittest
from app import create_app, db
from app.models import User, Entry
from app.forms import SignupForm
from app.config import TestConfig

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
    
    def test_invalid_email(self):
        """
        Test that a user cannot be created with an invalid email.
        """
        form_entry = SignupForm(name="Slacker", username="definitely_unique_user", age="20", gender="Male", email="skipperisaslacker", password="I_wanna_be_like_Skipper")
        form_entry.validate()
        self.assertIn("Please enter a valid email address", form_entry.email.errors)
    
    def test_password_length(self):
        form_entry = SignupForm(name="Peppa", username="peppa_pid", age="4", gender="Female", email="peppa@pig.com", password="count")
        form_entry.validate()
        self.assertIn("Field must be at least 6 characters long.", form_entry.password.errors)