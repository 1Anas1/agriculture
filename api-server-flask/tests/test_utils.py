import unittest
from flask import Flask
from app.utils.auth import hash_password, check_password
from app.utils.validation import validate_request

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a minimal Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def test_password_hashing(self):
        password = "securepassword"
        hashed = hash_password(password)
        self.assertTrue(check_password(hashed, password))

    def test_validate_request(self):
        # Use the application context for the test
        with self.app.app_context():
            data = {"field1": "value1", "field2": "value2"}
            required_fields = ["field1", "field2"]

            # Test case where all fields are present
            is_valid, error = validate_request(required_fields, data)
            self.assertTrue(is_valid)
            self.assertIsNone(error)

            # Test case where some fields are missing
            required_fields = ["field1", "field3"]
            is_valid, error = validate_request(required_fields, data)
            self.assertFalse(is_valid)
            self.assertIsNotNone(error)
