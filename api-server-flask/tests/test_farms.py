import unittest
from app.utils.db import get_collection
from app.config import TestingConfig
import json
from app import create_app, mongo


class FarmsTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the app with the testing configuration
        self.app = create_app(config_class=TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Seed test data
        with self.app.app_context():
            self.farms = get_collection('farms')
            self.farms.delete_many({})  # Clear existing test data
            self.farms.insert_many([
    {
        "_id": "farm1",
        "name": "Farm 1",
        "location": {"coordinates": [34.052235, -118.243683]}  # Los Angeles
    },
    {
        "_id": "farm2",
        "name": "Farm 2",
        "location": {"coordinates": [34.052245, -118.243693]}  # Nearby Los Angeles
    },
    {
        "_id": "farm3",
        "name": "Farm 3",
        "location": {"coordinates": [36.778259, -119.417931]}  # Fresno (far away)
    }
]

)

    def tearDown(self):
        # Clean up after the test
        with self.app.app_context():
            self.farms.delete_many({})  # Clear test data
        mongo.cx.close()
        self.ctx.pop()

    def test_check_nearby_farms(self):
    # Test case: Farm 1 with a 5 km radius
        response = self.client.get('/farms/farm1/check-nearby-diseases?radius_km=5')
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data['farms']), 1)  
        farm_names = [farm['name'] for farm in data['farms']]
        self.assertIn("Farm 2", farm_names)
        self.assertNotIn("Farm 3", farm_names) 
