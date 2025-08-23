# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_label # Corrected import

app = FastAPI(title="GitHub Issue Triage API")

# This is a Pydantic model for our input data
class Issue(BaseModel):
    title: str
    body: str

@app.on_event("startup")
def load_model_and_tokenizer():
    """Load the model and tokenizer into the application state on startup."""
    # This is a placeholder, as our predictor.py already loads the model globally.
    # In a more complex app, you would load it here.
    print("Application startup complete. Model is loaded.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the GitHub Issue Triage API. Model is loaded."}

@app.post("/triage")
def triage_issue(issue: Issue):
    text_input = f"[TITLE]: {issue.title} [BODY]: {issue.body}"
    predicted_label = predict_label(text_input)
    return {"predicted_label": predicted_label}
