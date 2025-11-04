# doctor_rag/rag_server.py

from fastapi import FastAPI, Request
from create_embeddings import process_patient
import uvicorn

app = FastAPI()

@app.post("/update_embedding")
async def update_embedding(request: Request):
    data = await request.json()
    patient_id = data.get("patient_id")
    process_patient(patient_id)
    return {"status": "Embedding updated", "patient_id": patient_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
