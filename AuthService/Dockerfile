FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies and verify uvicorn is installed
RUN pip install --no-cache-dir -r requirements.txt && \
    pip show uvicorn

# Copy the rest of the application
COPY . .

# Using python -m uvicorn
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8001"]