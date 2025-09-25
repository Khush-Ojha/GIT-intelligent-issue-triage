# predictor.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Use the absolute paths inside the container
TOKENIZER_PATH = "/code/tokenizer"
MODEL_PATH = "/code/model"

# Load the tokenizer and our fine-tuned classification model
print("Loading classification model...")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
id2label = model.config.id2label
print("Classification model loaded successfully.")

def predict_label(text: str) -> str:
    """
    Takes a string of text and returns the predicted label.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]