import unittest
from app import create_app
from app.utils.db import get_collection

class FarmsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.farms = get_collection('farms')
        self.farms.delete_many({})

    def test_check_nearby_farms(self):
        farm_id = self.farms.insert_one({
            "user_id": "123",
            "location": {"type": "Point", "coordinates": [12.34, 56.78]},
            "plants": []
        }).inserted_id

        # Insert another farm nearby
        self.farms.insert_one({
            "user_id": "456",
            "location": {"type": "Point", "coordinates": [12.35, 56.79]},
            "plants": []
        })

        response = self.client.get(f'/farms/{farm_id}/check-nearby-diseases?radius_km=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json['farms']) > 0)
