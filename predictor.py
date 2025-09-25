# predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F # We need this for the softmax function

# --- Load Models ---
TOKENIZER_PATH = "tokenizer"
MODEL_PATH = "model"

print(f"Loading tokenizer from local path: {TOKENIZER_PATH}")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
print(f"Loading fine-tuned model from local path: {MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
print("Model and tokenizer loaded successfully.")
id2label = model.config.id2label

# --- Old Prediction Function (kept for reference) ---
def predict_label(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

# --- NEW ADVANCED PREDICTION FUNCTION ---
def predict_probabilities(text: str) -> dict:
    """
    This function takes text and returns a dictionary of all labels
    and their corresponding confidence scores (probabilities).
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Convert raw model scores (logits) into probabilities
    probabilities = F.softmax(logits, dim=1).squeeze().tolist()
    
    # Pair each label with its calculated probability
    results = {}
    for i, label in id2label.items():
        results[label] = probabilities[i]
        
    return results