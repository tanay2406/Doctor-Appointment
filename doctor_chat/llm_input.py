# # doctor_rag/format_patient_data.py

import os
import requests
from dotenv import load_dotenv
from google import generativeai as genai
from PIL import Image
from io import BytesIO

# 1️⃣ Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def download_report(report_url):
    """
    Downloads the medical report (image/pdf) from the Cloudinary link.
    Returns a file-like object (BytesIO).
    """
    try:
        response = requests.get(report_url)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"⚠️ Failed to download report: {report_url} | Error: {e}")
        return None
def extract_text_from_report(report_url):
    """
    Uses Gemini 2.5 Flash model to extract relevant medical text
    from image or PDF reports.
    """
    file_data = download_report(report_url)
    if not file_data:
        return ""

    model = genai.GenerativeModel("models/gemini-2.5-flash")

    try:
        # Detect file type
        url_lower = report_url.lower()
        prompt = (
            "You are a medical OCR assistant. "
            "Extract only relevant information such as test names, results, reference ranges, "
            "doctor's notes, and impressions from this report. Avoid decorative or unrelated text."
        )

        if url_lower.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(file_data)
            response = model.generate_content([prompt, image])

        elif url_lower.endswith(".pdf"):
            file_data.seek(0)
            response = model.generate_content([
                prompt,
                {"mime_type": "application/pdf", "data": file_data.read()}
            ])
        else:
            print("⚠️ Unsupported report format")
            return ""

        return response.text.strip() if response else ""

    except Exception as e:
        print(f"⚠️ Error extracting report text: {e}")
        return ""



def convert_patient_to_text(patient_data):
    """
    Converts MongoDB patient data into a clean, readable text format for LLM.
    Includes relevant extracted report information.
    """
    # Basic details
    text = (
        f"Patient ID: {patient_data.get('patientId', 'N/A')}\n"
        f"Name: {patient_data.get('name', 'N/A')}\n"
        f"Gender: {patient_data.get('gender', 'N/A')}\n"
        f"Age: {patient_data.get('age', 'N/A')}\n"
        f"Blood Group: {patient_data.get('bloodGroup', 'N/A')}\n"
        f"Symptoms: {patient_data.get('symptoms', 'N/A')}\n"
        f"Medical History: {patient_data.get('history', 'N/A')}\n"
        f"Ongoing Treatment: {patient_data.get('ongoingTreatment', 'N/A')}\n"
        f"Medications: {patient_data.get('medications', 'N/A')}\n"
        f"Allergies: {patient_data.get('allergies', 'N/A')}\n"
        f"Chronic Conditions: {patient_data.get('chronicConditions', 'N/A')}\n\n"
        "---- Extracted Report Details ----\n"
    )

    # Extract from reports (if available)
    reports = patient_data.get("reports", [])
    for i, url in enumerate(reports, 1):
        print(f"📄 Processing report {i}...")
        extracted_text = extract_text_from_report(url)
        if extracted_text:
            text += f"Report {i}:\n{extracted_text}\n\n"
        else:
            text += f"Report {i}: [No readable data found]\n\n"

    return text


# Example test
if __name__ == "__main__":
    genai.list_models()  # To verify API connectivity
    # Example dummy data
    patient = {
        "_id": "6908a75b98a82a3f74d8fde9",
        "patientId": "68ecdf80bf84e35493306732",
        "name": "Tanay Lalwani",
        "gender": "Male",
        "age": 20,
        "bloodGroup": "O+",
        "symptoms": "Exhausted badly",
        "history": "no",
        "ongoingTreatment": "no",
        "medications": "dolo",
        "allergies": "acne",
        "chronicConditions": "yes",
        "reports": [
            "https://res.cloudinary.com/dfvfq35ba/image/upload/v1762248690/patient_reports/Screenshot%202025-11-04%20140706.png.png"
        ]
    }

    formatted_text = convert_patient_to_text(patient)
    print("\nFinal LLM Input Text:\n")
    print(formatted_text)


