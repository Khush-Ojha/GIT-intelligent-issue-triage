# predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# Define paths
TOKENIZER_PATH = "./tokenizer"
MODEL_PATH = "./model"
CACHE_PATH = "/tmp/hf_cache" # Writable directory on the HF server

# --- CLASSIFICATION MODEL (Existing) ---
print("Loading classification model...")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
id2label = model.config.id2label
print("Classification model loaded.")


# --- SUMMARIZATION MODEL (New, with the fix) ---
print("Loading summarization model...")
# We tell the pipeline to use our writable cache directory
summarizer = pipeline("summarization", model="t5-small", model_kwargs={"cache_dir": CACHE_PATH})
print("Summarization model loaded.")


# --- Prediction Functions ---
def predict_label(text: str) -> str:
    """Takes a string of text and returns the predicted label."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

def summarize_text(text: str) -> str:
    """Takes a long string of text and returns a one-sentence summary."""
    summary = summarizer(text, max_length=60, min_length=10, do_sample=False)
    return summary[0]['summary_text']