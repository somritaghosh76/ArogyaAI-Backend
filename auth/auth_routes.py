from flask import Blueprint, request, jsonify
from firebase_admin import auth
import datetime

# Define the Blueprint
auth_bp = Blueprint('auth', __name__)

# 🔹 Login Route (Now Uses GET Instead of POST)
@auth_bp.route("/login", methods=["GET"])
def login():
    # Extract email & password from URL parameters
    email = request.args.get("email")
    password = request.args.get("password")

    # Validate request
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # 🔹 Fetch user from Firebase Auth
        user = auth.get_user_by_email(email)

        # ✅ Generate a Firebase authentication token instead of create_access_token
        custom_token = auth.create_custom_token(user.uid).decode("utf-8")
        return jsonify({"message": "Login successful", "token": custom_token}), 200

    except auth.UserNotFoundError:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Error during login: {str(e)}")  # Log error for debugging
        return jsonify({"error": "An error occurred. Please try again."}), 500
