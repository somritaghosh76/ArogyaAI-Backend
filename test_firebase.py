import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebase_admin_sdk.json")  # Ensure this file exists
firebase_admin.initialize_app(cred)

print("✅ Firebase Initialized Successfully!")
