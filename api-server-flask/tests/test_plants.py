import unittest
from app import create_app
from app.utils.db import get_collection

class PlantsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.plants = get_collection('plants')
        self.diseases = get_collection('diseases')
        self.plants.delete_many({})
        self.diseases.delete_many({})

    def test_detect_disease(self):
        plant_id = self.plants.insert_one({
            "farm_id": "123",
            "name": "Plant A",
            "disease_records": [],
            "current_condition": "Healthy"
        }).inserted_id

        response = self.client.post(f'/plants/{plant_id}/detect-disease', json={
            "disease_name": "Fungal Infection",
            "treatment": "Apply fungicide",
            "image_url": "http://example.com/image.jpg",
            "follow_up_in_days": 10
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Disease detected", response.json['message'])
