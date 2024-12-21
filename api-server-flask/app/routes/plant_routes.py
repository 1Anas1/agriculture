from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.plant_service import detect_disease, get_user_plants, get_plant_treatment_details

plant_bp = Blueprint('plants', __name__)

@plant_bp.route('/<plant_id>/detect-disease', methods=['POST'])
@jwt_required()
def detect_disease_route(plant_id):
    try:
        # Parse input data
        data = request.get_json()

        # Validate required fields
        required_fields = ["disease_name", "treatment", "image_base64", "follow_up_in_days"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Get the current user ID from the JWT token
        user_id = get_jwt_identity()

        # Call the service
        result = detect_disease(
            user_id=user_id,
            plant_id=plant_id,
            disease_name=data['disease_name'],
            treatment=data['treatment'],
            image_base64=data['image_base64'],
            follow_up_in_days=data['follow_up_in_days']
        )

        # Return the result
        return jsonify(result), 200
    except Exception as e:
        # Log the error details
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@plant_bp.route('/user-plants', methods=['GET'])
@jwt_required()
def get_user_plants_route():
    """
    Endpoint to get all plants for the authenticated user.
    """
    try:
        # Get the current user ID from the JWT token
        user_id = get_jwt_identity()

        # Retrieve the user's plants
        plants = get_user_plants(user_id)
        return jsonify(plants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@plant_bp.route('/<plant_id>/treatment-details', methods=['GET'])
@jwt_required()
def get_plant_treatment_details_route(plant_id):
    """
    Endpoint to get treatment details for a specific plant.
    """
    try:
        # Call service to get treatment details
        treatment_details = get_plant_treatment_details(plant_id)
        return jsonify(treatment_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
