from flask import Flask
from flask_cors import CORS
from auth.auth_routes import auth_bp  # Import authentication routes
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


# 🔹 Firebase Initialization (Prevent Multiple Initializations)
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\somri\Desktop\arogyaai-backend\firebase_admin_sdk.json.json")  # Ensure correct path
    firebase_admin.initialize_app(cred)

# 🔹 Register Authentication Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Running on all interfaces
