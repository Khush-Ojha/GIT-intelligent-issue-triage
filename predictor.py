# predictor.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# --- THE FIX: Use relative paths that work on your local machine ---
TOKENIZER_NAME = "tokenizer"
MODEL_PATH = "model"

# Load the tokenizer from your local 'tokenizer' folder
print(f"Loading tokenizer from local path: {TOKENIZER_NAME}")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

# Load our fine-tuned model from the local 'model' folder
print(f"Loading fine-tuned model from local path: {MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
print("Model and tokenizer loaded successfully.")

id2label = model.config.id2label

def predict_label(text: str) -> str:
    """
    This function takes a string of text and returns the predicted label.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id2label[predicted_class_id]

# This block is for local testing
if __name__ == '__main__':
    test_text_bug = "[TITLE]: Login button not working [BODY]: The button is broken."
    test_text_feature = "[TITLE]: Add dark mode [BODY]: Please add a dark theme."
    print("\n--- Running a quick local test ---")
    prediction_1 = predict_label(test_text_bug)
    print(f"Prediction for 'bug' text: '{prediction_1}'")
    prediction_2 = predict_label(test_text_feature)
    print(f"Prediction for 'enhancement' text: '{prediction_2}'")