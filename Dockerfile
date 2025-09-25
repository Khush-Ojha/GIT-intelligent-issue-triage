FROM python:3.11-slim

WORKDIR /code

# Install git and git-lfs
RUN apt-get update && apt-get install -y git git-lfs

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the model and app files
COPY ./model /code/model
COPY ./app /code/app

# Copy the main app file
COPY app.py .

# Set environment variables
ENV MODEL_PATH="/code/model"

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]