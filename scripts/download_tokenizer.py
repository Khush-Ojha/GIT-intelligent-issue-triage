# scripts/download_tokenizer.py
from transformers import AutoTokenizer

model_name = "microsoft/deberta-v3-base"
save_directory = "tokenizer"

print(f"Downloading tokenizer for '{model_name}'...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

print(f"Tokenizer saved to '{save_directory}' folder successfully.")