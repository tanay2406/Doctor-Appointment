# doctor_rag/create_embeddings.py

from fetch_data import get_patient_data
from prepare_text import patient_json_to_text
from vector_db import add_or_update_patient_embedding
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_text_embedding(text):
    """Create embeddings using Gemini API."""
    model = "models/embedding-001"
    result = genai.embed_content(model=model, content=text)
    return result['embedding']

def process_patient(patient_id):
    """Fetch, prepare, and store patient embedding."""
    patient = get_patient_data(patient_id)
    if not patient:
        print("❌ No patient found.")
        return

    text = patient_json_to_text(patient)
    embedding = get_text_embedding(text)
    add_or_update_patient_embedding(patient_id, embedding, text)

if __name__ == "__main__":
    # Example test
    process_patient("6908e1b6d8db373099b027f8")
