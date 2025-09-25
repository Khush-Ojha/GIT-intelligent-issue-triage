FROM python:3.11-slim

WORKDIR /code

# Install git and git-lfs
RUN apt-get update && apt-get install -y git git-lfs

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model directories
COPY ./model /code/model
COPY ./tokenizer /code/tokenizer
COPY ./summarization_model /code/summarization_model

# Copy remaining application files
COPY . .

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]