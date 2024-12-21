from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import decode_token

def hash_password(password):
    """Hash a plain text password."""
    return generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, plain_password):
    """Verify a plain text password against its hash."""
    return check_password_hash(hashed_password, plain_password)

def decode_jwt_token(token):
    """Decode a JWT token to extract the payload."""
    try:
        return decode_token(token)
    except Exception as e:
        return None
