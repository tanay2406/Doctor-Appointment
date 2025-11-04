import os
from dotenv import load_dotenv
import google.generativeai as genai
from create_embeddings import get_text_embedding
from fetch_data import get_patient_data
from prepare_text import patient_json_to_text
from vector_db import get_relevant_patient_text


# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- RAG CHAT PIPELINE ---------- #

def retrieve_relevant_info(question):
    query_embedding = get_text_embedding(question)
    results = get_relevant_patient_text(query_embedding)
    if results and results["documents"]:
        return results["documents"][0][0]  # best match
    return "No relevant info found."


def generate_answer(question, context):
    """Use Gemini model to answer based on context + question."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a medical assistant for doctors. 
    Use the following patient context to answer the question.

    PATIENT CONTEXT:
    {context}

    QUESTION:
    {question}

    Please give a clear and medically relevant response.
    """
    response = model.generate_content(prompt)
    return response.text


def chat_with_patient(patient_id, question):
    """Main function to run doctor query through RAG system."""
    patient = get_patient_data(patient_id)
    if not patient:
        return "No data found for that patient."

    # Convert JSON to text (with OCR done inside)
    patient_text = patient_json_to_text(patient)

    # Retrieve relevant info
    relevant_info = retrieve_relevant_info(question)
    if not relevant_info:
        return "Could not retrieve relevant info."

    # Generate answer
    answer = generate_answer(question, relevant_info)
    return answer


# -------------- TEST --------------- #
if __name__ == "__main__":
    # Replace this with the actual patientId you want to query
    patient_id = "6908e1b6d8db373099b027f8"

    print("Doctor Chat System Ready")
    while True:
        question = input("\nDoctor: ")
        if question.lower() in ["exit", "quit"]:
            print("Ending chat.")
            break
        answer = chat_with_patient(patient_id, question)
        print("\n🤖 AI:", answer)
