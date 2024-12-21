from app.models.notification import Notification

def get_user_notifications(user_id):
    return Notification.get_notifications_by_user(user_id)

def mark_notification_as_read(notification_id):
    Notification.update_notification(notification_id, {"status": "Read"})
