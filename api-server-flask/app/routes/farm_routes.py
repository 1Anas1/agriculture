from flask import Blueprint, request, jsonify
from app.services.farm_service import get_nearby_farms

farm_bp = Blueprint('farms', __name__)

@farm_bp.route('/<farm_id>/check-nearby-diseases', methods=['GET'])
def check_nearby_diseases(farm_id):
    radius_km = float(request.args.get('radius_km', 5))  # Default radius is 5 km
    try:
        farms = get_nearby_farms(farm_id, radius_km)
        return jsonify({"farms": farms}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
