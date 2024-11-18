# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure uvicorn is in requirements.txt
RUN pip install uvicorn

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]