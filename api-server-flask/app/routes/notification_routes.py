from flask import Blueprint, request
from app.services.notification_service import get_user_notifications, mark_notification_as_read

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
def fetch_notifications():
    user_id = request.args.get('user_id')
    notifications = get_user_notifications(user_id)
    return {"notifications": notifications}, 200

@notification_bp.route('/<notification_id>/mark-read', methods=['POST'])
def mark_as_read(notification_id):
    mark_notification_as_read(notification_id)
    return {"message": "Notification marked as read"}, 200
