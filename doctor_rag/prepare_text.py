import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_image(image_url: str) -> str:
    """Extract text from an image URL using Gemini Vision model."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([image_url, "Extract all text visible in this medical report image."])
        text = response.text
        return text.strip() if text else "No readable text found."
    except Exception as e:
        print(f"OCR failed for {image_url}: {e}")
        return "OCR failed or no readable content."

def patient_json_to_text(patient_data: dict) -> str:
    """Convert patient JSON into readable text with OCR-enhanced reports."""

    lines = []
    lines.append(f"Patient Name: {patient_data.get('name', 'Unknown')}")
    lines.append(f"Patient ID: {patient_data.get('patientId', 'N/A')}")
    lines.append(f"Gender: {patient_data.get('gender', 'N/A')}")
    lines.append(f"Age: {patient_data.get('age', 'N/A')}")
    lines.append(f"Blood Group: {patient_data.get('bloodGroup', 'N/A')}")
    lines.append(f"Symptoms: {patient_data.get('symptoms', 'N/A')}")
    lines.append(f"History: {patient_data.get('history', 'N/A')}")
    lines.append(f"Ongoing Treatment: {patient_data.get('ongoingTreatment', 'N/A')}")
    lines.append(f"Medications: {patient_data.get('medications', 'N/A')}")
    lines.append(f"Allergies: {patient_data.get('allergies', 'N/A')}")
    lines.append(f"Chronic Conditions: {patient_data.get('chronicConditions', 'N/A')}")

    # Handle reports with OCR
    reports = patient_data.get('reports', [])
    if reports and isinstance(reports, list):
        lines.append("Reports Text Extracted via OCR:")
        for i, report_url in enumerate(reports, start=1):
            lines.append(f"  Report {i} URL: {report_url}")
            ocr_text = extract_text_from_image(report_url)
            lines.append(f"  Report {i} Extracted Text: {ocr_text}\n")
    else:
        lines.append("Reports: None")

    lines.append(f"Record Created At: {patient_data.get('createdAt', 'N/A')}")
    return "\n".join(lines)
