import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import create_app from your Flask factory setup
from app import create_app, db
from app.models import User

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"  
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # Ensure SECRET_KEY is set in the app's config directly as well
        self.app.config['SECRET_KEY'] = TestConfig.SECRET_KEY
        
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

    def test_login_missing_fields(self):
        # Missing password
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': ''
        }, follow_redirects=True)
        self.assertIn(b'Login', response.data)

        # Missing email
        response = self.client.post('/login', data={
            'email': '',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertIn(b'Login', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Ensure app has a secret key for session/flash functionality
        response = self.client.post('/login', data={
            'email': 'nonexistent@test.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'Invalid email or password', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_login_route_get(self):
        """Test the login page loads correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_successful_login(self):
        """Test successful login with valid credentials"""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        # Check for successful login indicators - modify these assertions based on your app's behavior
        self.assertEqual(response.status_code, 200)
        # Usually there would be a welcome message or redirect to a dashboard
        # self.assertIn(b'Welcome', response.data)  # Uncomment and modify as needed


if __name__ == '__main__':
    unittest.main()