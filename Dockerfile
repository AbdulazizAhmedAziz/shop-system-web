# Dockerfile for Railway deployment
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (Railway will set PORT env variable)
EXPOSE 8080

# Run application (Railway sets PORT automatically)
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120

