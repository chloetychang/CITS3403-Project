import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import create_app from your Flask factory setup
from app import create_app, db
from app.models import User

class TestLogin(unittest.TestCase):
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
    
    


if __name__ == '__main__':
    unittest.main()