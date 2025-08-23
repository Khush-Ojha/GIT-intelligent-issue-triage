# app/predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# --- THE FINAL FIX: Use the writable /tmp directory for the cache ---
TOKENIZER_NAME = "/code/tokenizer" 
MODEL_PATH = "/code/model"
CACHE_PATH = "/tmp/hf_cache" # This is a standard writable directory in cloud environments

# Load the tokenizer from Hub, using our specified cache path
print(f"Loading tokenizer '{TOKENIZER_NAME}' from Hub...")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME, cache_dir=CACHE_PATH)

# Load our fine-tuned model from the local path
print(f"Loading fine-tuned model from path: {MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
print("Model and tokenizer loaded successfully.")

id2label = model.config.id2label

def predict_label(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

# This block is for local testing and won't run on the server
if __name__ == '__main__':
    test_text_bug = "[TITLE]: Login button not working [BODY]: The button is broken."
    test_text_feature = "[TITLE]: Add dark mode [BODY]: Please add a dark theme."
    print("\n--- Running a quick local test ---")
    prediction_1 = predict_label(test_text_bug)
    print(f"Prediction for 'bug' text: '{prediction_1}'")
    prediction_2 = predict_label(test_text_feature)
    print(f"Prediction for 'enhancement' text: '{prediction_2}'")