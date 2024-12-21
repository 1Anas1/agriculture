from flask import Blueprint, request
from app.services.plant_service import detect_disease

plant_bp = Blueprint('plants', __name__)

@plant_bp.route('/<plant_id>/detect-disease', methods=['POST'])
def detect_disease_route(plant_id):
    data = request.get_json()
    return detect_disease(
        plant_id,
        data['disease_name'],
        data['treatment'],
        data['image_url'],
        data['follow_up_in_days']
    )
