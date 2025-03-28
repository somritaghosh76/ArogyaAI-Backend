import os
import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
from deep_translator import GoogleTranslator  # ✅ Use deep-translator

# 🔹 Load Firebase Credentials
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# 🔹 Initialize Google Translator Wrapper
def translate_text_google(text, target_lang):
    """Translate text using deep-translator (Google Translate API)."""
    try:
        translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return translated_text.strip().lower()  # Ensure lowercase and no extra spaces
    except Exception as e:
        st.error(f"Google Translation Error: {e}")
        return text.strip().lower()  # Fallback to original text

# 🔹 Fallback Dictionary for Hindi to English (if Google Translate Fails)
hindi_to_english_dict = {
    "खांसना": "cough",
    "बुखार": "fever",
    "सिरदर्द": "headache",
    "गले में खराश": "sore throat"
}

def translate_with_fallback(text):
    """Try API translation, else use dictionary."""
    translated = translate_text_google(text, "en")
    
    # If translation failed or returned the same text, use dictionary
    if translated == text:
        translated = hindi_to_english_dict.get(text, text)
    
    return translated

# 🔹 Language Selection
languages = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta"
}

selected_lang = st.selectbox("Choose your language:", list(languages.keys()))
target_lang = languages[selected_lang]

# 🔹 Path to dataset directory
data_dir = "data/"

def load_datasets():
    """Load the dataset containing symptom descriptions."""
    dataset_path = os.path.join(data_dir, "symptom_Description.csv")
    if os.path.exists(dataset_path):
        try:
            df = pd.read_csv(dataset_path)
            st.success("✅ " + translate_text_google("Dataset loaded successfully!", target_lang))
            return df
        except Exception as e:
            st.error(translate_text_google("Error loading dataset:", target_lang) + f" {e}")
            return None
    else:
        st.error(translate_text_google(f"⚠ Dataset file '{dataset_path}' not found!", target_lang))
        return None

# 🔹 Streamlit UI
st.title("🩺 " + translate_text_google("ArogyaAI - AI-Powered Disease Prediction Chatbot", target_lang))

# 🔹 Authentication
email = st.text_input(translate_text_google("Enter your email", target_lang), key="email_input")
password = st.text_input(translate_text_google("Enter your password", target_lang), type="password", key="password_input")

if st.button(translate_text_google("Login", target_lang), key="login_button"):
    try:
        user = auth.get_user_by_email(email)
        st.success(translate_text_google("Welcome", target_lang) + f" {user.email}!")
    except:
        st.error(translate_text_google("User not found. Please register first.", target_lang))

# 🔹 Load dataset
df = load_datasets()

# 🔹 Chatbot Interface
st.subheader(translate_text_google("Chat with ArogyaAI", target_lang))
chat_history = st.session_state.get("chat_history", [])

# 🔹 User Input for Symptoms
user_input = st.text_input(translate_text_google("Enter your symptoms (comma-separated):", target_lang), key="symptom_input")

if st.button(translate_text_google("Predict Disease", target_lang), key="predict_button") and df is not None:
    if user_input:
        # Translate user input to English before matching
        translated_symptoms = []
        for symptom in user_input.split(","):
            translated = translate_text_google(symptom.strip(), "en")
            st.write(f"🔄 Translating '{symptom.strip()}' ➝ '{translated}'")  # Debugging line
            translated_symptoms.append(translated.lower())

        # Debugging: Display translated symptoms
        st.write("📝 Original Symptoms:", user_input.split(","))
        st.write("🔄 Translated Symptoms:", translated_symptoms)

        matched_diseases = []

        # Ensure correct dataset columns
        disease_col = "Drug Reaction" 
        symptom_col = "An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug or result from the combination of two or more drugs."  

        if disease_col not in df.columns or symptom_col not in df.columns:
            st.error("Dataset column names do not match. Please check the CSV file.")
        else:
            for _, row in df.iterrows():
                disease_name = row[disease_col]
                description = row[symptom_col]

                if isinstance(description, str):  # Ensure description is valid
                    # Match symptoms ignoring case differences
                    if any(symptom in description.lower() for symptom in translated_symptoms):
                        matched_diseases.append((disease_name, description))

        # Display results
        if matched_diseases:
            st.subheader(translate_text_google("Possible Conditions:", target_lang))
            for disease, desc in matched_diseases:
                disease_translated = translate_text_google(disease, target_lang)
                desc_translated = translate_text_google(desc, target_lang)
                st.write(f"🩺 {disease_translated}: {desc_translated}")
        else:
            st.info(translate_text_google("No matching diseases found based on provided symptoms.", target_lang))

        # Store chat history
        chat_history.append(f"👤 User: {user_input}")
        chat_history.append(f"🤖 ArogyaAI: {matched_diseases if matched_diseases else 'No match found.'}")
        st.session_state["chat_history"] = chat_history

# 🔹 Display Chat History
st.subheader(translate_text_google("Chat History:", target_lang))
for chat in chat_history:
    st.write(chat)