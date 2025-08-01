# Base Python image
FROM python:3.11-slim

# Set environment variables to avoid interactive prompts and reduce image size
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (including libpq for PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    redis \
    git \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip + torch first
RUN pip install --upgrade pip && \
    pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Then install requirements
COPY requirements.txt .
RUN pip install --default-timeout=300 --retries=5 --no-cache-dir -r requirements.txt


# Finally copy the source code
COPY . .

# Ensure init script is executable
RUN chmod +x /app/postgres-init/init.sql

# Expose FastAPI port
EXPOSE 8007

# Default run command (used only if docker-compose doesn't override it)
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8007"]
