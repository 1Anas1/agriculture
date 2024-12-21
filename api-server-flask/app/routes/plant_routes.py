from flask import Blueprint, request, jsonify
from app.services.plant_service import detect_disease

plant_bp = Blueprint('plants', __name__)

@plant_bp.route('/<plant_id>/detect-disease', methods=['POST'])
def detect_disease_route(plant_id):
    data = request.get_json()

    # Validate input
    required_fields = ["disease_name", "treatment", "image_url", "follow_up_in_days"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Call the service
    result = detect_disease(
        plant_id,
        data['disease_name'],
        data['treatment'],
        data['image_url'],
        data['follow_up_in_days']
    )

    # Return the result
    return jsonify(result), 200
