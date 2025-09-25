# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_label, summarize_text # Import both functions

app = FastAPI(title="GitHub Issue Triage & Summarization API")

class Issue(BaseModel):
    title: str
    body: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the GitHub Issue API"}

@app.post("/triage")
def triage_issue(issue: Issue):
    """Receives issue title and body, and returns the predicted label."""
    text_input = f"[TITLE]: {issue.title} [BODY]: {issue.body}"
    predicted_label = predict_label(text_input)
    return {"predicted_label": predicted_label}

@app.post("/summarize")
def summarize_issue(issue: Issue):
    """Receives issue title and body, and returns a one-sentence summary."""
    text_input = f"[TITLE]: {issue.title} [BODY]: {issue.body}"
    summary = summarize_text(text_input)
    return {"summary": summary}