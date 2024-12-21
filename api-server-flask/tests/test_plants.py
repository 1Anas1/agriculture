import unittest
import json
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from app import create_app
from app.config import TestingConfig

class PlantRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the application with testing configuration
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the application context

        self.client = self.app.test_client()

        # Create a mock user ID for authentication
        self.user_id = "test_user_id"
        self.access_token = create_access_token(identity=self.user_id)

    def tearDown(self):
        # Pop the application context
        self.app_context.pop()

    @patch('app.services.plant_service.detect_disease')
    def test_detect_disease_route(self, mock_detect_disease):
        # Mock the response from the detect_disease service
        mock_detect_disease.return_value = {
            "disease_name": "Leaf Blight",
            "follow_up_date": "2024-12-31T00:00:00",
            "symptoms": "yellowing leaf edges, black spots on leaves"
        }

        # Prepare the test data
        test_plant_id = "plant123"
        test_data = {
            "disease_name": "Leaf Blight",
            "treatment": "Apply fungicide",
            "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "follow_up_in_days": 10
        }

        # Make a POST request to the detect-disease route
        response = self.client.post(
            f"/plants/{test_plant_id}/detect-disease",
            headers={"Authorization": f"Bearer {self.access_token}"},
            data=json.dumps(test_data),
            content_type="application/json"
        )

        # Assert the response
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn("disease_name", response_data)
        self.assertIn("follow_up_date", response_data)
        self.assertIn("symptoms", response_data)
        self.assertEqual(response_data["disease_name"], "Leaf Blight")
        self.assertEqual(response_data["symptoms"], "yellowing leaf edges, black spots on leaves")

    @patch('app.services.plant_service.detect_disease')
    def test_detect_disease_route_missing_fields(self, mock_detect_disease):
        # Prepare incomplete test data
        test_plant_id = "plant123"
        test_data = {
            "disease_name": "Leaf Blight",
            # Missing treatment, image_base64, follow_up_in_days
        }

        # Make a POST request to the detect-disease route
        response = self.client.post(
            f"/plants/{test_plant_id}/detect-disease",
            headers={"Authorization": f"Bearer {self.access_token}"},
            data=json.dumps(test_data),
            content_type="application/json"
        )

        # Assert the response
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertIn("error", response_data)
        self.assertIn("Missing fields", response_data["error"])

if __name__ == "__main__":
    unittest.main()
