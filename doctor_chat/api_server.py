# doctor_chat/api_server.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from doctor_chat.fetch_data import get_patient_data
from doctor_chat.llm_input import convert_patient_to_text
from google import generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Model for incoming doctor request
class ChatRequest(BaseModel):
    patient_id: str
    doctor_query: str

@app.post("/start_chat")
async def start_chat(request: ChatRequest):
    """
    This endpoint automates your chatbot flow:
    1. Fetches patient data using the given ID.
    2. Converts it into a text input for the LLM.
    3. Sends the doctor’s query + patient context to Gemini.
    4. Returns the model’s response.
    """
    try:
        # Step 1: Fetch patient data
        patient_data = get_patient_data(request.patient_id)
        if not patient_data:
            return {"error": "Patient not found"}

        # Step 2: Convert to LLM input text
        patient_text = convert_patient_to_text(patient_data)

        # Step 3: Initialize chat model (with memory/history)
        model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
        chat = model.start_chat(history=[])

        # Step 4: Combine patient data + doctor query
        full_prompt = f"""
        You are a medical assistant chatbot. Use the following patient data:
        {patient_text}

        Doctor's question: {request.doctor_query}
        """

        response = chat.send_message(full_prompt)

        return {"response": response.text}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Doctor Chat API is running ✅"}
