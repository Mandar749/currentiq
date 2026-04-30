from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from config import EXAM_CONFIG
from digest import generate_digest
from mcq_generator import generate_mcqs
from evaluator import evaluate_answer
from news_fetcher import fetch_todays_headlines

app = FastAPI(title="CurrentIQ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DigestRequest(BaseModel):
    exam: str
    days: int = 1
    topic: Optional[str] = None

class MCQRequest(BaseModel):
    exam: str
    topic: str
    count: int = 5

class EvaluateRequest(BaseModel):
    question: str
    answer: str
    word_limit: int = 150

@app.get("/")
async def root():
    return {
        "message": "CurrentIQ API — Powered by Amazon Nova",
        "model": "amazon.nova-lite-v1:0",
        "exams": list(EXAM_CONFIG.keys())
    }

@app.get("/headlines")
async def get_headlines():
    headlines = await fetch_todays_headlines()
    return {"headlines": headlines}

@app.post("/digest")
async def get_digest(req: DigestRequest):
    if req.exam not in EXAM_CONFIG:
        raise HTTPException(400, f"Unknown exam: {req.exam}")
    return await generate_digest(req.exam, req.days, req.topic)

@app.post("/mcq")
async def get_mcqs(req: MCQRequest):
    if req.exam not in EXAM_CONFIG:
        raise HTTPException(400, f"Unknown exam: {req.exam}")
    return await generate_mcqs(req.exam, req.topic, req.count)

@app.post("/evaluate")
async def evaluate(req: EvaluateRequest):
    return await evaluate_answer(req.question, req.answer, req.word_limit)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)