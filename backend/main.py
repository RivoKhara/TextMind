from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

# Use a smaller model to avoid memory issues
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",  # small but good model
    framework="pt",
)

app = FastAPI(title="AI Text Summarizer")

# Enable CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class TextIn(BaseModel):
    text: str

@app.post("/summarize")
async def summarize_text(data: TextIn):
    text = data.text.strip()
    if not text:
        return {"summary": "No text provided."}

    try:
        # Summarize with truncation to avoid memory errors
        summary_result = summarizer(
            text,
            max_length=140,
            min_length=60,
            do_sample=False,
            truncation=True,
        )
        summary_text = summary_result[0]["summary_text"]
        return {"summary": summary_text}
    except Exception as e:
        return {"summary": f"Error during summarization: {str(e)}"}

