# predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# --- CLASSIFICATION MODEL (Existing) ---
TOKENIZER_PATH = "./tokenizer"
MODEL_PATH = "./model"

print("Loading classification model...")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
id2label = model.config.id2label
print("Classification model loaded.")


# --- SUMMARIZATION MODEL (New) ---
print("Loading summarization model...")
# We load a small, efficient T5 model pre-trained for summarization
summarizer = pipeline("summarization", model="t5-small")
print("Summarization model loaded.")


# --- Prediction Functions ---
def predict_label(text: str) -> str:
    """
    Takes a string of text and returns the predicted label.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

def summarize_text(text: str) -> str:
    """
    Takes a long string of text and returns a one-sentence summary.
    """
    # The pipeline handles all the complex tokenization and generation
    summary = summarizer(text, max_length=60, min_length=10, do_sample=False)
    # We extract just the summary text from the result
    return summary[0]['summary_text']