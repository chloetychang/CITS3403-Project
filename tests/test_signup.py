import unittest
from datetime import datetime
from app import create_app, db
from app.models import User
from app.forms import SignupForm
from werkzeug.datastructures import MultiDict
import os
import sys

# Get absolute path to project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TestSignUp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create dummy user for login tests
        user = User(name="Test", username="tester", age=25, gender="female", email="test@example.com")
        user.password = "testpass123"
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_and_password_hashing(self):
        """ Test user creation and password hashing works correctly."""
        response = self.client.post('/signup', data={
            'name': 'Test User',
            'username': 'testuser',
            'age': 20,
            'gender': 'female',
            'email': f'user{datetime.now().timestamp()}@test.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123'
        }, follow_redirects=True)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user, "User should be created in the database")
        self.assertNotEqual(user.password_hash, 'securepass123')
        self.assertTrue(user.check_password('securepass123'))

    def test_duplicate_email_registration(self):
        email = f'dupe{datetime.now().timestamp()}@test.com'
        user1 = User(name='First', username='firstuser', age=25, gender='female', email=email)
        user1.password = 'firstpass'
        db.session.add(user1)
        db.session.commit()

        response = self.client.post('/signup', data={
            'name': 'Second',
            'username': 'seconduser',
            'age': 22,
            'gender': 'female',
            'email': email,
            'password': 'secondpass',
            'confirm_password': 'secondpass'
        }, follow_redirects=True)

        users = User.query.filter_by(email=email).all()
        self.assertEqual(len(users), 1,)

    def test_duplicate_username_registration(self):
        username = "duplicateuser"
        user1 = User(name="User One", username=username, age=25, gender="female", email="user1@example.com")
        user1.password = "pass123"
        db.session.add(user1)
        db.session.commit()

        response = self.client.post("/signup", data={
            "name": "User Two",
            "username": username,
            "age": 28,
            "gender": "female",
            "email": f"user2{datetime.now().timestamp()}@example.com",
            "password": "pass1234",
            "confirm_password": "pass1234"
        }, follow_redirects=True)

        users_with_same_username = User.query.filter_by(username=username).all()
        self.assertEqual(len(users_with_same_username), 1,)
    
    def test_successful_signup_form(self):
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