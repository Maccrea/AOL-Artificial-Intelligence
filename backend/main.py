import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Muat variabel environment dari file .env
load_dotenv()

app = FastAPI(title="AI MVP Backend", version="1.0")

USE_LOCAL_AI = os.getenv("USE_LOCAL_AI", "True").lower() == "true"

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "AI Backend API Berjalan Mulus!", "mode": "Lokal" if USE_LOCAL_AI else "Cloud"}

@app.post("/api/ask")
async def ask_ai(req: PromptRequest):
    if USE_LOCAL_AI:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "dolphin-mistral",
            "prompt": req.prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return {
                "source": "Ollama (Local)",
                "answer": data.get("response", "")
            }
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Gagal menghubungi Ollama lokal: {str(e)}")

    else:
        return {
            "source": "Cloud API",
            "answer": "Mode Cloud aktif! (Kode integrasi Groq/Gemini belum diisi)."
        }