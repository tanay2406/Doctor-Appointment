import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_patient_data(patient_id="68ecdf80bf84e35493306732"):
    """Fetch a single patient's record from MongoDB Atlas"""
    patient = collection.find_one({"patientId": patient_id})

    if not patient:
        print(" No patient found with that ID.")
        return None

    # Convert ObjectId to string
    patient["_id"] = str(patient["_id"])

    # Convert MongoDB document to plain Python dict
    return patient


if __name__ == "__main__":
    data = get_patient_data()
    if data:
        print("✅ Patient data fetched successfully!")
        print(data)
