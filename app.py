# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_label

app = FastAPI(title="GitHub Issue Triage API")

class Issue(BaseModel):
    title: str
    body: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the GitHub Issue Triage API"}

@app.post("/triage")
def triage_issue(issue: Issue):
    text_input = f"[TITLE]: {issue.title} [BODY]: {issue.body}"
    predicted_label = predict_label(text_input)
    return {"predicted_label": predicted_label}