import pytest
from app import app, db
from app.models import User  # if needed

class TestLogin:
    def setup_method(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for test
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = app.test_client()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_login_missing_fields(self):
        """❌ Test login form submission with missing fields is rejected."""
        # Missing password
        response = self.client.post('/login', data={
            'email': 'login@test.com',
            'password': ''
        }, follow_redirects=True)

        assert b'Login' in response.data  # Page remains on login
        assert b'Email' in response.data  # Field labels present
        # You can also check for error messages if flashed

        # Missing email
        response = self.client.post('/login', data={
            'email': '',
            'password': 'testpass123'
        }, follow_redirects=True)

        assert b'Login' in response.data
