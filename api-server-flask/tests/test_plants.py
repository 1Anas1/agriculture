import unittest
import json
from app import create_app, mongo

class PlantsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='app.config.TestingConfig')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Clear the database to ensure isolated test cases
        with self.app.app_context():
            mongo.db.plants.delete_many({})
            mongo.db.diseases.delete_many({})
            mongo.db.notifications.delete_many({})

    def tearDown(self):
        mongo.cx.close()
        self.ctx.pop()

    def test_detect_disease(self):
        # Load test data
        with open('tests/data/plants_test_data.json') as f:
            test_data = json.load(f)

        data = test_data['detect_disease']['input']
        expected_status = test_data['detect_disease']['expected_status_code']
        expected_disease = test_data['detect_disease']['expected_disease_name']

        # Mock plant ID and make API call
        plant_id = data["plant_id"]

        # API call
        response = self.client.post(
            f'/plants/{plant_id}/detect-disease',
            json={
                "disease_name": data["disease_name"],
                "treatment": "Apply antifungal spray",
                "image_url": data["image_url"],
                "follow_up_in_days": 7
            }
        )

        # Assertions
        self.assertEqual(response.status_code, expected_status)
        self.assertIn("Blight", response.json.get("disease_name"))
