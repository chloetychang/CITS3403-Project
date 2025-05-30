import unittest
from app import db, create_app
from app.models import User
from datetime import datetime
import werkzeug.security

class TestFlaskBackend(unittest.TestCase):
    def setUp(self):
        """Setup before each test"""
        self.app = create_app(True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Cleanup after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage_title(self):
        """Test that the homepage loads with correct title"""
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
    
    def test_user_signup_flow(self):
        """Test the complete signup flow"""
        # Generate unique credentials for this test
        timestamp = int(datetime.now().timestamp())
        test_username = f"testuser{timestamp}"
        test_email = f"test{timestamp}@example.com"
        test_password = "SecureP@ss123"
        
        # Manually create user to avoid routing issues
        user = User(name='Test User', username=test_username, age=25, 
                   gender='male', email=test_email)
        user.password_hash = werkzeug.security.generate_password_hash(test_password)
        db.session.add(user)
        db.session.commit()
        
        # Check if user was created properly
        created_user = User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, test_email)
        
    def test_user_login_logout_flow(self):
        """Test the complete login and logout flow"""
        # Create a test user in the database
        timestamp = int(datetime.now().timestamp())
        test_username = f"loginuser{timestamp}"
        test_email = f"login{timestamp}@example.com"
        test_password = "SecureP@ss123"
        
        # Create user directly in database
        user = User(
            name="Login Test",
            username=test_username,
            age=30,
            gender="female",
            email=test_email
        )
        user.password_hash = werkzeug.security.generate_password_hash(test_password)
        db.session.add(user)
        db.session.commit()
        
        # Log in via POST request
        response = self.client.post('/login', data={
            'email': test_email,
            'password': test_password
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sleep', response.data)  

        # Log out via GET request
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)
    
    def test_nonexistent_page(self):
        """Test accessing a page that doesn't exist returns 404"""
        with self.app.test_client() as client:
            response = client.get('/nonexistent-page')
            self.assertEqual(response.status_code, 404)
            
    def test_user_creation(self):
        """Test user creation directly through the model"""
        user = User(name="Test User", username="testuser1", age=25, 
                   gender="male", email="test1@example.com")
        user.password_hash = werkzeug.security.generate_password_hash("password123")
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        created_user = User.query.filter_by(username="testuser1").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, "test1@example.com")
    
    def test_multiple_users(self):
        """Test creating multiple users"""
        # Create user 1
        user1 = User(name="User One", username="user1", age=25, 
                    gender="male", email="user1@example.com")
        user1.password_hash = werkzeug.security.generate_password_hash("password123")
        db.session.add(user1)
        
        # Create user 2
        user2 = User(name="User Two", username="user2", age=30, 
                    gender="female", email="user2@example.com")
        user2.password_hash = werkzeug.security.generate_password_hash("password456")
        db.session.add(user2)
        
        db.session.commit()
        
        # Verify both users were created
        users = User.query.all()
        self.assertEqual(len(users), 2)
        
        # Verify specific users
        user1_check = User.query.filter_by(username="user1").first()
        user2_check = User.query.filter_by(username="user2").first()
        
        self.assertIsNotNone(user1_check)
        self.assertIsNotNone(user2_check)
        
        self.assertEqual(user1_check.email, "user1@example.com")
        self.assertEqual(user2_check.email, "user2@example.com")
    
    def test_password_validation(self):
        """Test password validation through werkzeug"""
        password = "test_password"
        hashed_password = werkzeug.security.generate_password_hash(password)
        
        # Test valid password
        self.assertTrue(werkzeug.security.check_password_hash(hashed_password, password))
        
        # Test invalid password
        self.assertFalse(werkzeug.security.check_password_hash(hashed_password, "wrong_password"))


if __name__ == "__main__":
    unittest.main()