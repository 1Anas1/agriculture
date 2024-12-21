from flask import jsonify
from app.models.user import User
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_user(data):
    if User.find_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    user_data = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password,
        "farms": []
    }
    User.create_user(user_data)
    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    user = User.find_user_by_email(data['email'])

    # Use `check_password_hash` to compare the hashed password and the input password
    if user and check_password_hash(user['password'], data['password']):
        token = create_access_token(identity=str(user['_id']), expires_delta=timedelta(days=1))
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
