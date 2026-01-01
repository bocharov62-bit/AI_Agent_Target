# Landing Redesign Assistant
# Docker image for AI-agent that analyzes landing pages

FROM python:3.12-slim

# Metadata
LABEL maintainer="Bocharov62"
LABEL description="AI-agent for landing page analysis powered by GigaChat"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Default command (CLI mode)
ENTRYPOINT ["python", "agent.py"]

# Default arguments (can be overridden)
CMD ["--help"]

