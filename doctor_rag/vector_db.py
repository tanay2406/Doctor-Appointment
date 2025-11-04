# doctor_rag/vector_db.py

import chromadb

# Initialize a persistent ChromaDB client (saved in ./chroma_data folder)
chroma_client = chromadb.PersistentClient(path="./chroma_data")

def get_or_create_collection():
    """Create or get existing 'patients' collection."""
    return chroma_client.get_or_create_collection(name="patients")

def add_or_update_patient_embedding(patient_id, embedding, text):
    """Add or update embedding for a patient."""
    collection = get_or_create_collection()
    # Use patient_id as the unique document ID
    collection.upsert(
        ids=[str(patient_id)],
        embeddings=[embedding],
        documents=[text]
    )
    print(f"✅ Embedding added/updated for patient {patient_id}")

def get_relevant_patient_text(question_embedding, top_k=1):
    """Retrieve most relevant patient context."""
    collection = get_or_create_collection()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )
    return results
