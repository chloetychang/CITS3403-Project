import pytest
from datetime import datetime
from app import app, db
from app.models import User

class TestSignUp:
    def setup_method(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = app.test_client()

    def teardown_method(self):
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

        print(response.data.decode())  # helpful if debugging
        user = User.query.filter_by(username='testuser').first()
        assert user is not None, "User should be created in the database"
        assert user.password_hash != 'securepass123'
        assert user.check_password('securepass123')

    def test_duplicate_email_registration(self):
        """❌ Test duplicate email registration is rejected."""
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
        assert len(users) == 1, "❌ Duplicate email should not allow a second account"

    def test_duplicate_username_registration(self):
        """❌ Test duplicate username registration is rejected."""
        username = 'duplicateuser'

        user1 = User(name='User One', username=username, age=30, gender='female', email='user1@example.com')
        user1.password = 'pass1'
        db.session.add(user1)
        db.session.commit()

        response = self.client.post('/signup', data={
            'name': 'User Two',
            'username': username,
            'age': 28,
            'gender': 'female',
            'email': f'user2{datetime.now().timestamp()}@example.com',
            'password': 'pass2',
            'confirm_password': 'pass2'
        }, follow_redirects=True)

        users = User.query.filter_by(username=username).all()
        assert len(users) == 1, "❌ Duplicate username should not allow a second account"
