# doctor_rag/fetch_data.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB credentials from .env
MONGO_URI = os.getenv("MONGO_URI")          # your MongoDB Atlas connection string
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  # your database name
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")  # your collection name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION]


def get_patient_data(patient_id: str):
    """
    Fetch patient data from MongoDB using their unique ID.
    Returns a Python dictionary.
    """
    try:
        # Find document by _id or patientId
        patient = collection.find_one({"patientId": patient_id}) or collection.find_one({"_id": patient_id})
        
        if not patient:
            print(f"❌ No patient found with ID {patient_id}")
            return None

        # Convert ObjectId to string for JSON compatibility
        if "_id" in patient:
            patient["_id"] = str(patient["_id"])

        print(f"✅ Patient data fetched successfully for ID {patient_id}")
        return patient

    except Exception as e:
        print("⚠️ Error fetching patient data:", e)
        return None


if __name__ == "__main__":
    # Example test
    sample_id = "68ecdf80bf84e35493306732"
    patient = get_patient_data(sample_id)
    if patient:
        print(patient)
