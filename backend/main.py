from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import torch

# Use CPU only
device = -1  # -1 means CPU

# Load smaller summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    framework="pt",
    device=device
)

app = FastAPI(title="AI Text Summarizer")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class TextIn(BaseModel):
    text: str

@app.post("/summarize")
async def summarize_text(data: TextIn):
    text = data.text.strip()
    if not text:
        return {"summary": "No text provided."}

    summary = summarizer(
        text,
        max_length=140,
        min_length=60,
        do_sample=False,
        truncation=True
    )[0]["summary_text"]

    return {"summary": summary}
