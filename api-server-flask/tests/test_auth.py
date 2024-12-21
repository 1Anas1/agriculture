import unittest
from app import create_app
from app.utils.db import get_collection

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['MONGO_URI'] = "mongodb://localhost:27017/test_database"  # Use a test database
        self.client = self.app.test_client()

        # Use the application context
        with self.app.app_context():
            self.users = get_collection('users')
            self.users.delete_many({})  # Clear test data

    def test_register_user(self):
        response = self.client.post('/auth/register', json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.json['message'])

    def test_login_user(self):
        # First, register a user
        self.users.insert_one({
            "name": "Test User",
            "email": "test@example.com",
            "password": "hashed_password"
        })
        response = self.client.post('/auth/login', json={
            "email": "test@example.com",
            "password": "hashed_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)
