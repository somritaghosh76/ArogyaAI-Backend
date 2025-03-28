from flask_jwt_extended import create_access_token

def generate_token(user_id):
    """Generates a JWT token for the given user ID."""
    return create_access_token(identity=user_id)
