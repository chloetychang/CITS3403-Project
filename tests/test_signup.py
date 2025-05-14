import unittest
from datetime import datetime
import os
import sys

# Get absolute path to project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Define TestConfig within the test file
class TestConfig:
    SECRET_KEY = 'test-secret-key'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

from app import create_app, db
from app.models import User

class TestSignUp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app.config['SECRET_KEY'] = TestConfig.SECRET_KEY
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_user_creation_and_password_hashing(self):
        """✅ Test user creation and password hashing works correctly."""
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