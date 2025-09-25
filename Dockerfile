# Use a modern, stable Python version
FROM python:3.11-slim

# Set the working directory
WORKDIR /code

# Install git and git-lfs
RUN apt-get update && apt-get install -y git git-lfs

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application files and models
# This is the corrected part
COPY . .

# Expose the port
EXPOSE 7860

# The command to run our application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]