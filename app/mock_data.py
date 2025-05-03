from werkzeug.security import generate_password_hash

# Mock database (replace with real DB later i.e. db that stores username and pw data.)
# Attaching mock database to app instance
users = {
    "test@example.com": {
        "password": generate_password_hash("password123", method='pbkdf2:sha256'),  # ← Explicit method
        "name": "Test User",
        "username": "testuser"
    }
}