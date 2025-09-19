# predictor.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

TOKENIZER_PATH = "./tokenizer"
MODEL_PATH = "./model"

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
id2label = model.config.id2label

def predict_label(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]