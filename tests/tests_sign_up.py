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
    
    def test_duplicate_email(self):
        pass
    
    def test_duplicate_username(self):
        pass