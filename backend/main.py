import os
import requests
from io import BytesIO
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if not SARVAM_API_KEY:
    raise ValueError("Missing SARVAM_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://paper-summarizer-ruddy.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ArxivRequest(BaseModel):
    pdf_url: str


# -----------------------------
# Extract PDF
# -----------------------------
def extract_text_from_pdf_url(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    response.raise_for_status()

    pdf_file = BytesIO(response.content)
    reader = PdfReader(pdf_file)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# Chunk
# -----------------------------
def chunk_text(text: str, max_length: int = 6000):
    chunks = []
    while len(text) > max_length:
        split_at = text.rfind(" ", 0, max_length)
        if split_at == -1:
            split_at = max_length
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        chunks.append(text)
    return chunks


# -----------------------------
# Generate Report
# -----------------------------
def generate_report(text_chunks):

    condensed_text = "\n\n".join(text_chunks[:3])

    system_prompt = """
    You are an expert reporter. 
    Your task is to grasp the core conepts and insights from the paper
    And present it clearly with bold keywords
    """

    user_prompt = f"""
        Grasp the contents from this text and generate a report with the following format:
    {condensed_text}
    In this format :
    Title: "fill in the title"
    What is the problem being addressed?
    Why is it important?
    Novelty: What is the novel contribution of this paper?
    Results and Conclusions
    """

    response = requests.post(
        "https://api.sarvam.ai/v1/chat/completions",
        headers={
            "api-subscription-key": SARVAM_API_KEY,
        },
        json={
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "model": "sarvam-m",
            "max_tokens": 2000
        },
    )

    output = response.json()
    return output["choices"][0]["message"]["content"]


# -----------------------------
# API Route
# -----------------------------
@app.post("/generate-report")
def generate(request: ArxivRequest):
    try:
        raw_text = extract_text_from_pdf_url(request.pdf_url)
        chunks = chunk_text(raw_text)
        report = generate_report(chunks)

        return {"report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
