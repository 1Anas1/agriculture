from app.utils.db import get_collection

class Notification:
    @staticmethod
    def create_notification(data):
        notifications = get_collection('notifications')
        notifications.insert_one(data)

    @staticmethod
    def get_notifications_by_user(user_id):
        notifications = get_collection('notifications')
        return list(notifications.find({"user_id": user_id}))

    @staticmethod
    def update_notification(notification_id, update_data):
        notifications = get_collection('notifications')
        notifications.update_one({"_id": notification_id}, {"$set": update_data})
