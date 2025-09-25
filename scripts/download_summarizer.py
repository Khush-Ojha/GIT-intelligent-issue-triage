# scripts/download_summarizer.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "t5-small"
save_directory = "summarization_model"

print(f"Downloading model and tokenizer for '{model_name}'...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"Summarization model saved to '{save_directory}' folder successfully.")