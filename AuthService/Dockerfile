FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The application code will be mounted as a volume during development
# so we don't need to COPY it here

# Command to run the application with hot-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]