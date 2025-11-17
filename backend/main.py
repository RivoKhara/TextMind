from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

# Load model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    framework="pt"
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

    # IMPROVED SETTINGS
    summary = summarizer(
        text,
        max_length=140,      # increased (default ~60)
        min_length=60,       # ensure it's not too short
        do_sample=False,     # deterministic output
        truncation=True      # prevents model errors
    )[0]["summary_text"]

    return {"summary": summary}
