import os

class Config:
    MONGO_URI = "mongodb://localhost:27017/plant_disease_management"
    JWT_SECRET_KEY = "your_jwt_secret_key"
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
class TestingConfig(Config):
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/test_database"
