import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Project, Message

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio backend running"}

@app.get("/api/projects")
async def list_projects(limit: int = 12):
    if db is None:
        # Return sample data if DB not configured
        sample = [
            {"title": "Realtime anomaly monitor", "tags": ["Time-series", "Streaming", "Dash"], "summary": "Detect anomalies on IoT feeds; Kafka + Prophet + fast dashboards."},
            {"title": "Generative report assistant", "tags": ["LLM", "RAG", "LangChain"], "summary": "Retrieves domain docs and drafts analyst-ready summaries."},
            {"title": "Marketing mix modeling", "tags": ["Bayesian", "PyMC"], "summary": "Media ROI attribution with uncertainty-aware recommendations."}
        ]
        return {"projects": sample}

    docs = get_documents("project", {}, limit)
    # Normalize ObjectId for JSON
    for d in docs:
        d["id"] = str(d.get("_id"))
        d.pop("_id", None)
    return {"projects": docs}

@app.post("/api/contact")
async def contact(msg: Message):
    if db is None:
        # No DB: just echo success
        return {"message": "Thanks for reaching out, I'll get back to you soon."}

    try:
        create_document("message", msg)
        return {"message": "Thanks for reaching out, I'll get back to you soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available" if db is None else "✅ Connected",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Connected" if db is not None else "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["collections"] = db.list_collection_names()[:10]
    except Exception as e:
        response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
