from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .utils.db import init_db

# Extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    if config_class:
        app.config.from_object(config_class)

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app
