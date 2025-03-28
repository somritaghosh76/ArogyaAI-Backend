import os
import firebase_admin
from firebase_admin import credentials, auth

# 🔹 Get the absolute path of the current script's directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CRED_PATH = os.path.join(BASE_DIR, r"C:\Users\somri\Desktop\arogyaai-backend\firebase_admin_sdk.json.json")  # Construct the full path

# 🔹 Load Firebase credentials securely
if not firebase_admin._apps:  # Ensure Firebase is not initialized multiple times
    if not os.path.exists(CRED_PATH):
        raise FileNotFoundError(f"⚠ Firebase credential file missing at: {CRED_PATH}")
    
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)
