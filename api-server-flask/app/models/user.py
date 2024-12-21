from app.utils.db import get_collection

class User:
    @staticmethod
    def create_user(data):
        users = get_collection('users')
        users.insert_one(data)

    @staticmethod
    def find_user_by_email(email):
        users = get_collection('users')
        return users.find_one({"email": email})

    @staticmethod
    def find_user_by_id(user_id):
        users = get_collection('users')
        return users.find_one({"_id": user_id})
