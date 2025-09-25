# predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
import torch

# --- THE FIX: Use absolute paths inside the Docker container ---
CLASSIFICATION_TOKENIZER_PATH = "/code/tokenizer"
CLASSIFICATION_MODEL_PATH = "/code/model"
SUMMARIZATION_MODEL_PATH = "/code/summarization_model"

# --- CLASSIFICATION MODEL ---
print("Loading classification model...")
classification_tokenizer = AutoTokenizer.from_pretrained(CLASSIFICATION_TOKENIZER_PATH)
classification_model = AutoModelForSequenceClassification.from_pretrained(CLASSIFICATION_MODEL_PATH)
id2label = classification_model.config.id2label
print("Classification model loaded.")

# --- SUMMARIZATION MODEL ---
print("Loading summarization model...")
summarization_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZATION_MODEL_PATH)
summarization_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZATION_MODEL_PATH)
summarizer = pipeline(
    "summarization", 
    model=summarization_model, 
    tokenizer=summarization_tokenizer
)
print("Summarization model loaded.")

# --- Prediction Functions ---
def predict_label(text: str) -> str:
    inputs = classification_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = classification_model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

def summarize_text(text: str) -> str:
    summary = summarizer(text, max_length=60, min_length=10, do_sample=False)
    return summary[0]['summary_text']