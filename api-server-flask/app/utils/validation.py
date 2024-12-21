from flask import jsonify

def validate_request(required_fields, data):
    """
    Validate if the required fields are present in the request data.
    Args:
        required_fields: List of field names that must be present in the data.
        data: The data to validate.
    Returns:
        A tuple (is_valid, error_message)
    """
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return False, jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    return True, None
