import unittest
from app import create_app
from app.config import TestingConfig
from app.utils.auth import hash_password, check_password
from app.utils.validation import validate_request
from app import mongo  # Import the MongoDB instance

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the app with the testing configuration
        self.app = create_app(config_class=TestingConfig)
        self.client = self.app.test_client()

        # Push the application context
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Clear MongoDB collections if needed for tests
        with self.app.app_context():
            # Example: Clear users collection (add if needed for test data cleanup)
            # mongo.db.users.delete_many({})
            pass

    def tearDown(self):
        # Close the MongoClient if initialized
        if hasattr(mongo, 'cx') and mongo.cx:
            mongo.cx.close()  # Close the MongoClient explicitly
        self.ctx.pop()  # Pop the application context

    def test_password_hashing(self):
        # Test hashing and checking passwords
        password = "securepassword"
        hashed = hash_password(password)
        self.assertTrue(check_password(hashed, password))

    def test_validate_request(self):
        # Use the application context for validation logic
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
