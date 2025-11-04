# doctor_rag/chat_pipeline.py
from google import generativeai as genai
from dotenv import load_dotenv
import os



from fetch_data import get_patient_data
from llm_input import convert_patient_to_text

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


# -----------------------------
# STEP 1: Initialize chat model
# -----------------------------
def create_chat_session():
    """
    Creates a new Gemini chat session.
    The model keeps track of previous messages automatically.
    """
    model = model = genai.GenerativeModel("models/gemini-2.0-flash-lite") # or gemini-1.5-pro if you want deeper reasoning
    chat = model.start_chat(history=[])
    print("✅ Chat session initialized.")
    return chat


# -----------------------------
# STEP 2: Start doctor chat
# -----------------------------
def doctor_chat(patient_id):
    """
    Doctor chat pipeline:
    - Fetches patient data
    - Formats data into text
    - Starts chat session with Gemini
    - Lets doctor ask follow-up questions
    """

    # 1️⃣ Fetch data
    patient_data = get_patient_data(patient_id)
    if not patient_data:
        print("❌ Patient not found.")
        return

    # 2️⃣ Convert to LLM-friendly text
    patient_text = convert_patient_to_text(patient_data)
    print("\n🩺 Patient data converted successfully.\n")

    # 3️⃣ Initialize chat
    chat = create_chat_session()

    # 4️⃣ Provide patient context to the model
    system_prompt = (
        "You are an AI medical assistant helping a doctor analyze patient data. "
        "Use the provided patient details and extracted report text to give accurate, "
        "safe, and helpful medical insights. Always include reasoning clearly."
    )

    # Send patient context to the model (hidden message)
    chat.send_message(f"{system_prompt}\n\nPATIENT DATA:\n{patient_text}")

    print("✅ Patient data sent to chat model.\n")

    # 5️⃣ Interactive chat loop for the doctor
    print("👨‍⚕️ Doctor Chat Started (type 'exit' to quit)\n")

    while True:
        doctor_query = input("Doctor: ")
        if doctor_query.lower() in ["exit", "quit"]:
            print("🩺 Chat ended.")
            break

        # Pass doctor query to model
        response = chat.send_message(doctor_query)

        # Display AI reply
        print("\n🤖 AI Assistant:", response.text, "\n")


# -----------------------------
# TESTING / MAIN ENTRY
# -----------------------------
if __name__ == "__main__":
    # Example test
    test_patient_id = "68ecdf80bf84e35493306732"
    doctor_chat(test_patient_id)
