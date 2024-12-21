import unittest
from app import create_app
from app.utils.db import get_collection

class NotificationsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.notifications = get_collection('notifications')
        self.notifications.delete_many({})

    def test_fetch_notifications(self):
        user_id = "123"
        self.notifications.insert_one({
            "user_id": user_id,
            "message": "Test notification",
            "status": "Pending",
            "date_created": "2024-01-01"
        })

        response = self.client.get(f'/notifications?user_id={user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json['notifications']) > 0)

    def test_mark_notification_as_read(self):
        notification_id = self.notifications.insert_one({
            "user_id": "123",
            "message": "Test notification",
            "status": "Pending",
            "date_created": "2024-01-01"
        }).inserted_id

        response = self.client.post(f'/notifications/{notification_id}/mark-read')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Notification marked as read", response.json['message'])
