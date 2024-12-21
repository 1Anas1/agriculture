from flask import Blueprint
from .auth_routes import auth_bp
from .plant_routes import plant_bp
from .farm_routes import farm_bp
from .notification_routes import notification_bp

# Aggregate all blueprints
def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(plant_bp, url_prefix='/plants')
    app.register_blueprint(farm_bp, url_prefix='/farms')
    app.register_blueprint(notification_bp, url_prefix='/notifications')
