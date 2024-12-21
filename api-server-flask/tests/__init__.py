import pytest
from app import create_app

@pytest.fixture
def app():
    """Create a Flask app instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/test_plant_disease_management"
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()
