import unittest
from app import create_app, db
from app.models import User
from app.forms import LoginForm
from werkzeug.datastructures import MultiDict

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
        
    def test_successful_login_form(self):
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

    def test_login_validation_form(self):
        """
        Test that users can only log in with all required fields filled in.
        To run test: python -m unittest tests.tests_login.TestLogin.test_login_validation
        """
        form_entry = LoginForm(formdata=MultiDict({
            "email":"skipper@example.com"
        }))
        self.assertFalse(form_entry.validate())
        self.assertIn("This field is required.", form_entry.password.errors)
    
    
if __name__ == '__main__':
    unittest.main()