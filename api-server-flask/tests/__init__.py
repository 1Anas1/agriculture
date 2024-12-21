import pytest
from app import create_app, mongo
from flask import Flask

@pytest.fixture(scope='module')
def app():
    """Create a Flask app instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/test_plant_disease_management"

    # Push application context for the module
    ctx = app.app_context()
    ctx.push()

    yield app  # Provide the app instance to the tests

    # Teardown: Close the MongoClient and pop the context
    mongo.cx.close()
    ctx.pop()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()
