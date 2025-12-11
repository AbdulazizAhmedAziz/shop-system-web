# Dockerfile for Railway deployment
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (Railway will set PORT env variable)
EXPOSE $PORT

# Run application
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120

