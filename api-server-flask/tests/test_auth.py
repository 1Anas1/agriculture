import unittest
import json
from app import create_app, mongo
from flask_bcrypt import generate_password_hash
from app.utils.db import get_collection

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='app.config.TestingConfig')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Clear database and set up users collection
        with self.app.app_context():
            self.users = get_collection('users')
            self.users.delete_many({})

    def tearDown(self):
        mongo.cx.close()
        self.ctx.pop()

    def test_register_user(self):
        # Load test data
        with open('tests/data/auth_test_data.json') as f:
            test_data = json.load(f)

        data = test_data['register_user']['input']
        expected_status = test_data['register_user']['expected_status_code']
        expected_message = test_data['register_user']['expected_message']

        # Make API call
        response = self.client.post('/auth/register', json=data)

        # Assertions
        self.assertEqual(response.status_code, expected_status)
        self.assertIn(expected_message, response.json['message'])

    def test_login_user(self):
        # Load test data
        with open('tests/data/auth_test_data.json') as f:
            test_data = json.load(f)

        # Insert user into database
        with self.app.app_context():
            self.users.insert_one({
                "name": "Test User",
                "email": "test@example.com",
                "password": generate_password_hash("password123").decode('utf-8')
            })

        data = test_data['login_user']['input']
        expected_status = test_data['login_user']['expected_status_code']
        expected_token_key = test_data['login_user']['expected_token_key']

        # Make API call
        response = self.client.post('/auth/login', json=data)

        # Assertions
        self.assertEqual(response.status_code, expected_status)
        self.assertIn(expected_token_key, response.json)
