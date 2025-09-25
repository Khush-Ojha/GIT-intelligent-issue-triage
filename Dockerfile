# Use a modern, stable Python version
FROM python:3.11-slim

# Set the working directory inside the server
WORKDIR /code

# Install Git and Git-LFS so the server can download our large model files
RUN apt-get update && apt-get install -y git git-lfs

# Copy and install all the Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application code and models from our project root
COPY . .

# Open the port that the application will run on
EXPOSE 7860

# The final command to start our FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]